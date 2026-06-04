
"""SEO sitemap generators for Google Search Console.



Sitemaps:

    - StaticViewSitemap: home, browse, FAQ pages (high priority)

    - ListingSitemap:    visi aktyvūs skelbimai (auto-update)

    - BrandSitemap:      brand pages (/?brand=X)

    - CategorySitemap:   category pages (cars, trucks, motorcycles)

"""

from django.contrib.sitemaps import Sitemap

from django.urls import reverse

from django.utils import timezone

from datetime import timedelta

from .models import Listing, Brand, VehicleType





class StaticViewSitemap(Sitemap):

    """Static pages: home, FAQ, contact."""

    priority = 1.0

    changefreq = 'daily'

    protocol = 'https'



    def items(self):

        return ['home', 'faq', 'contact']



    def location(self, item):

        try:

            return reverse(item)

        except Exception:

            if item == 'home':

                return '/'

            return f'/{item}/'





class ListingSitemap(Sitemap):

    """All active listings (excluding shadow-banned)."""

    changefreq = 'daily'

    priority = 0.8

    protocol = 'https'

    limit = 5000  # max URLs per sitemap file



    def items(self):

        return Listing.objects.filter(

            status='active',

            is_shadow_banned=False,

        ).order_by('-created_at')



    def lastmod(self, obj):

        return obj.updated_at if hasattr(obj, 'updated_at') and obj.updated_at else obj.created_at



    def location(self, obj):

        return f'/{obj.pk}/'





class CategorySitemap(Sitemap):

    """Category pages: /?category=cars, /?category=trucks, etc."""

    changefreq = 'weekly'

    priority = 0.7

    protocol = 'https'



    def items(self):

        return VehicleType.objects.filter(

            slug__in=['cars', 'trucks', 'motorcycles']

        )



    def location(self, obj):

        return f'/?category={obj.slug}'





class BrandSitemap(Sitemap):

    """Top brand pages (brands with 1+ active listings)."""

    changefreq = 'weekly'

    priority = 0.6

    protocol = 'https'



    def items(self):

        # Tik brand'ai kurie turi bent 1 aktyvų skelbimą

        active_brand_ids = Listing.objects.filter(

            status='active',

            is_shadow_banned=False,

        ).values_list('brand_id', flat=True).distinct()



        return Brand.objects.filter(id__in=active_brand_ids).order_by('name')



    def location(self, obj):

        return f'/?brand={obj.pk}'

