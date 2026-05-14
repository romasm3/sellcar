with open('templates/listings/listing_select_plan.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Surask PIRMĄ "(function()" - čia yra mūsų plano JS
idx = content.find('(function()')
if idx < 0:
    print('NOT FOUND - (function() neegzistuoja')
else:
    # Surask `<script>` prieš jį
    script_start = content.rfind('<script>', 0, idx)
    # Surask `</script>` po jo
    script_end = content.find('</script>', idx)
    
    if script_start < 0 or script_end < 0:
        print('Script tags not found')
    else:
        block = content[script_start:script_end + len('</script>')]
        # Print with line numbers
        # Pirma surask pradinę eilutę
        line_start = content[:script_start].count('\n') + 1
        for i, line in enumerate(block.split('\n')):
            print(f'{line_start + i}: {line}')