def print_symbols_table(symbols):
  print('final symbols table:')
  for symbol in symbols:
    print('----------')
    print(symbol)
    print('')
    for key in symbols[symbol]:
      value = symbols[symbol][key]
      if key != 'type_info':
        print(f"{f'{key}':<20}{f'{value}':>15}")
        
    print('')
    print_type_info(symbols[symbol]['type_info'])

def print_type_info(type_info):
  print('type info:')
  for item in type_info:
    print(f"{f'  {item}':<20}{f'{type_info[item]}':>15}")

def print_functions(symbols):
  print()
  print('----------')
  print()
  print('functions list: {')
  for symbol in symbols:
    if symbols[symbol]['symbol_type'] == 'function':
      print(' ',symbol,',')
  print('}')
