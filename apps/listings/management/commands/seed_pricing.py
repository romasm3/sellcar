with open('templates/listings/listing_select_plan.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Surask PIRMĄ <script> kuris turi (function() {)
in_script = False
script_start = -1
for i, line in enumerate(lines, start=1):
    if '<script>' in line and not in_script:
        in_script = True
        script_start = i
    if in_script and '(function()' in line:
        # Found the right script
        # Print from script_start to next </script>
        for j in range(script_start - 1, len(lines)):
            print(f'{j+1}: {lines[j]}', end='')
            if '</script>' in lines[j]:
                break
        break