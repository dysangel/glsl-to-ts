

function str(lines: (): = {}

current_line = 1
block_depth = 0
last_block_depth = 0

tokens_to_process = []

in_define = False
in_struct = False

final_tokens = []

for i in range(len(tokens)):
  token = tokens[i]
  last_token = tokens[i-1] if i > 1 else ''
   
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
   
  if token == ';

const function_list = {
  str,
}

export interface Api {
str: (lines: () => =
}