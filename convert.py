from util.parse import clean_tokens, count_char, process_define, process_block_header, process_statement, tokenise
from util.print import print_functions, print_symbols_table
from util.output import formatted_api_function_list, formatted_function_list

import sys

input_file = str(sys.argv[1])

with open(input_file) as f:
  lines = f.readlines()

tokens = tokenise(lines)
symbols = {}

current_line = 1
block_depth = 0
last_block_depth = 0

tokens_to_process = []

in_define = False
in_struct = False
in_comment = False

final_tokens = []

for i in range(len(tokens)):
  token = tokens[i]
  last_token = tokens[i-1] if i > 1 else ''
  
  if token == '/':
    if last_token == '/':
      in_comment = True
  
  if in_comment:
    tokens_to_process.append(token)
    
    if token == '\n':
      final_tokens.extend(tokens_to_process)
      tokens_to_process.clear()
      in_comment = False
  else: # not in comment
    if token == '#define':
      final_tokens.extend(tokens_to_process)
      tokens_to_process.clear()
      in_define = True

      #print('block_depth', block_depth)
      
    if in_define and token == '\n' and last_token != '\\':
      final_tokens.extend(tokens_to_process)
      in_define = False
      process_define(tokens_to_process)
      tokens_to_process.clear()

    tokens_to_process.append(token)
    
    if token == '{':
      if block_depth == 0:
        #tokens_to_process.pop()
        processed_block = process_block_header(symbols, tokens_to_process, block_depth)
        new_symbol = processed_block['symbols']
        symbols.update(new_symbol)
        print('new_symbol', new_symbol)
        symbol_type = ''
        for key in new_symbol:
          symbol_type = new_symbol[key]['symbol_type']
        if symbol_type == 'function':
          final_tokens.extend(['\n\n',processed_block['ts_block_header']])
        else:
          if symbol_type == 'struct':
            in_struct = True
          final_tokens.extend(tokens_to_process)
        tokens_to_process.clear()
      else:
        final_tokens.extend(tokens_to_process)
        tokens_to_process.clear()
      block_depth += 1
      
    if token == '}':
      in_struct = False
      final_tokens.extend(tokens_to_process)
      block_depth -= 1
      tokens_to_process.clear()
      #print('block_depth', block_depth)
      
    if token == ';':
      processed_tokens = process_statement(tokens_to_process, block_depth, in_struct)
      final_tokens.extend(processed_tokens)
      tokens_to_process.clear()
  #print('processed token', token, 'block depth is', block_depth)

#print_symbols_table(symbols)
#print_functions(symbols)

with open('output.ts', 'w') as f:
    f.write(''.join(final_tokens))
    f.write(formatted_function_list(symbols))
    f.write(formatted_api_function_list(symbols))
