def formatted_function_list(symbols):
  function_list = ['\n\nconst function_list = {']
  
  for symbol in sorted(symbols):
    if symbols[symbol]['symbol_type'] == 'function':
      function_list.append(f'  {symbol},')
  function_list.append('}')
  
  return '\n'.join(function_list)


def formatted_api_function_list(symbols):
  function_list = ['\n\nexport interface Api {']
  
  max_length = 0
  
  for symbol in sorted(symbols):
    if symbols[symbol]['symbol_type'] == 'function':
      if (len(symbol) > max_length):
        max_length = len(symbol)
  
  max_length += 2
  
  for symbol in sorted(symbols):
    if symbols[symbol]['symbol_type'] == 'function':
      function_name = f'{symbol}:'
      api_definition = symbols[symbol]['ts_api_type']
      function_list.append(f"{f'{function_name}':<{max_length}}{f'{api_definition}'}")
  function_list.append('}')
  
  return '\n'.join(function_list)
  