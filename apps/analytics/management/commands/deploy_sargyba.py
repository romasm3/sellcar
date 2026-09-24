# -*- coding: utf-8 -*-
"""
DEPLOY SARGYBINIS — ar įdiegta versija dar seka origin/master.

Kodėl reikia. 2026-09 deploy'as stovėjo AŠTUONIAS PARAS, ir to nepastebėjo
niekas: timeris sukosi kas minutę, krito ties švarumo patikra ir tylėjo,
nes tyla yra jo normalus elgesys (žr. deploy-from-git.sh antraštę).
Svetainė rodė rugsėjo 14 d. kodą, o master'yje gulėjo vienuolika commit'ų.
Vienintelis ženklas buvo <meta name="versija"> titulinio kode — bet į jį
reikia specialiai žiūrėti.

Sargybinis tą žiūrėjimą atlieka kasdien ir, atsilikus daugiau nei parą,
parašo laišką. Tikrinama TIK atsilikimo trukmė, ne commit'ų kiekis:
dešimt commit'ų per valandą yra normalu, o vienas commit'as, gulintis
parą — jau sugedęs deploy'as.

Paleidimas:
    python manage.py deploy_sargyba              # tikrina ir, jei reikia, rašo
    python manage.py deploy_sargyba --parodyk    # tik parodo, nesiunčia
    python manage.py deploy_sargyba --valandos 6

Automatiškai: deploy/systemd/autoleft-sargyba.timer (kasdien 08:00).
"""
import subprocess

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.utils import timezone

# Grandinės bandymas 2026-09-24: push → master → autoleft.com.
# Šios trys eilutės elgsenos nekeičia — tai žymė, pagal kurią matyti,
# ar commit'as iš viso pasiekė serverį.
# Po tiek valandų atsilikimas laikomas gedimu, ne normaliu darbu.
RIBA_VALANDOMIS = 24
GAVEJAS = 'romasm3@gmail.com'
# Kiek paskutinių deploy žurnalo eilučių įdėti į laišką.
ZURNALO_EILUCIU = 40


def _git(*argumentai):
    """git komanda projekto kataloge; tuščia eilutė, jei nepavyko."""
    try:
        return subprocess.check_output(
            ('git', '-C', str(settings.BASE_DIR)) + argumentai,
            stderr=subprocess.DEVNULL, timeout=60,
        ).decode('utf-8', 'replace').strip()
    except (subprocess.SubprocessError, OSError):
        return ''


def _git_yra(*argumentai):
    """Ar git komanda pavyko.

    Atskirai nuo `_git`, nes `cat-file -e` sekmes atveju NIEKO nespausdina
    — tikrinant pagal išvestį, sėkmė atrodydavo kaip klaida ir sargybinis
    būtų rašęs laišką kasdien be reikalo.
    """
    try:
        return subprocess.call(
            ('git', '-C', str(settings.BASE_DIR)) + argumentai,
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60,
        ) == 0
    except (subprocess.SubprocessError, OSError):
        return False


def paskutine_klaida():
    """Paskutinės deploy žurnalo eilutės — be jų laiškas nieko nepasako.

    journalctl serveryje yra, konteineryje ir vietinėje aplinkoje — ne;
    tokiu atveju tiesiog pasakom, kad žurnalo nėra, o ne meluojam.
    """
    try:
        isvestis = subprocess.check_output(
            ('journalctl', '-u', 'autoleft-deploy.service',
             '-n', str(ZURNALO_EILUCIU), '--no-pager'),
            stderr=subprocess.DEVNULL, timeout=60,
        ).decode('utf-8', 'replace').strip()
        return isvestis or '(žurnalas tuščias)'
    except (subprocess.SubprocessError, OSError):
        return '(journalctl nepasiekiamas — žiūrėk serveryje rankomis)'


def bukle(riba_valandomis=RIBA_VALANDOMIS):
    """{'atsilieka': bool, 'commitu': int, 'valandu': float, ...}

    Įdiegta versija imama iš settings.GIT_SHA — tos pačios, kurią rodo
    <meta name="versija">. Taip sargybinis mato lygiai tą patį, ką
    lankytojas, o ne tai, ką rodo .git.
    """
    _git('fetch', '--quiet', 'origin', 'master')

    idiegta = (getattr(settings, 'GIT_SHA', '') or '').strip()
    master = _git('rev-parse', 'origin/master')

    duomenys = {
        'idiegta': idiegta or 'nezinoma',
        'master': master[:12] if master else 'nezinoma',
        'commitu': 0,
        'valandu': 0.0,
        'atsilieka': False,
        'riba': riba_valandomis,
    }
    if not master or not idiegta or idiegta == 'nezinoma':
        duomenys['pastaba'] = 'nepavyko nustatyti versijų — patikrink rankomis'
        duomenys['atsilieka'] = True
        return duomenys

    # Ar įdiegtas commit'as apskritai žinomas šiam klonui?
    if not _git_yra('cat-file', '-e', '%s^{commit}' % idiegta):
        duomenys['pastaba'] = ('įdiegtas commit\'as %s nerastas repozitorijoje'
                               % idiegta)
        duomenys['atsilieka'] = True
        return duomenys

    kiek = _git('rev-list', '--count', '%s..origin/master' % idiegta)
    duomenys['commitu'] = int(kiek) if kiek.isdigit() else 0
    if duomenys['commitu'] == 0:
        return duomenys

    # Kiek laiko gula SENIAUSIAS neįdiegtas commit'as — nuo jo ir
    # skaičiuojam atsilikimą.
    seniausias = _git('log', '--reverse', '--format=%ct',
                      '%s..origin/master' % idiegta)
    pirma = seniausias.split('\n')[0] if seniausias else ''
    if pirma.isdigit():
        sekundziu = timezone.now().timestamp() - int(pirma)
        duomenys['valandu'] = round(sekundziu / 3600.0, 1)
    duomenys['atsilieka'] = duomenys['valandu'] > riba_valandomis
    return duomenys


def laisko_tekstas(d):
    eilutes = [
        'AutoLeft deploy\'as atsilieka.',
        '',
        'Įdiegta svetainėje: %s' % d['idiegta'],
        'origin/master:      %s' % d['master'],
        'Neįdiegta commit\'ų: %d' % d['commitu'],
        'Seniausias gula:    %.1f val. (riba %d val.)' % (d['valandu'], d['riba']),
    ]
    if d.get('pastaba'):
        eilutes += ['', 'Pastaba: %s' % d['pastaba']]
    eilutes += [
        '',
        'Neįdiegti commit\'ai:',
        _git('log', '--oneline', '%s..origin/master' % d['idiegta']) or '(nepavyko)',
        '',
        'Paskutinės deploy žurnalo eilutės:',
        paskutine_klaida(),
        '',
        'Rankinis paleidimas serveryje:',
        '    cd /root/autoleft && ./deploy-from-git.sh',
    ]
    return '\n'.join(eilutes)


class Command(BaseCommand):
    help = 'Tikrina, ar įdiegta versija seka origin/master; atsilikus rašo laišką.'

    def add_arguments(self, parser):
        parser.add_argument('--valandos', type=int, default=RIBA_VALANDOMIS,
                            help='po kiek valandų laikyti gedimu (numatyta 24)')
        parser.add_argument('--parodyk', action='store_true',
                            help='tik parodo, laiško nesiunčia')
        parser.add_argument('--gavejas', default=GAVEJAS)

    def handle(self, *args, **nust):
        d = bukle(nust['valandos'])
        self.stdout.write('idiegta=%s master=%s commitu=%d valandu=%.1f'
                          % (d['idiegta'], d['master'], d['commitu'], d['valandu']))
        if d.get('pastaba'):
            self.stdout.write('pastaba: %s' % d['pastaba'])

        if not d['atsilieka']:
            self.stdout.write(self.style.SUCCESS('Deploy\'as neatsilieka — tylim.'))
            return

        tekstas = laisko_tekstas(d)
        if nust['parodyk']:
            self.stdout.write('\n--- laiškas (nesiųstas) ---\n' + tekstas)
            return

        send_mail(
            subject='AutoLeft: deploy atsilieka %d commit\'ais (%.0f val.)'
                    % (d['commitu'], d['valandu']),
            message=tekstas,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[nust['gavejas']],
            fail_silently=False,
        )
        self.stdout.write(self.style.WARNING('Laiškas išsiųstas: %s' % nust['gavejas']))
