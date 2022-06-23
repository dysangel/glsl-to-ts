import re
  
def process_define(tokens):
  tokens = clean_tokens(tokens)
  print('define: ', tokens)
  
def process_block_header(symbols, original_tokens, block_depth):
  tokens = clean_tokens(original_tokens)
  ts_version = ''
  
  if len(tokens) == 0:
    return {}
    
  new_symbols = {}
  if tokens[0] == 'struct':
    struct = tokens[1]
    print('----------\nstruct definition')
    print('symbol:',struct)
    new_symbols[struct] = {
      'symbol_type': 'struct',
      'type_info': {
        'glsl_type': struct,
        'ts_type': struct[0].upper() + (struct[1:len(struct)]),
        'block_depth': 0,
      }
    }
    print(new_symbols[struct])
  else:
    start_index = find_open_parenthesis_index(tokens)
    close_index = find_close_parenthesis_index(tokens)
    if start_index > 1:
      print('----------\nfunction definition')
      print('symbol:',tokens[start_index - 1])
      symbol = tokens[start_index - 1]

      type_info = get_type_info(symbols, tokens[0: start_index - 1], block_depth)
      
      print('process_block_header tokens', tokens[start_index + 1: close_index])
      print('')
      args = process_args(symbols, tokens[start_index + 1: close_index], block_depth)
      print('symbol info is', type_info)
      ts_version = make_ts_function(symbol, type_info, args)
      ts_api_type = make_ts_api_function_definition(symbol, type_info, args)
      new_symbols[symbol] = {
        'symbol_type': 'function',
        'type_info': type_info,
        'args': args,
        'ts_version': ts_version,
        'ts_api_type': ts_api_type,
      }
      print('-------------\n', ts_version,'\n-------------')
    elif start_index > -1:
      print('weird open parenthesis position for tokens: ', tokens)
      
  return {
    'symbols': new_symbols,
    'ts_block_header': ts_version,
  }

def make_ts_args(args):
  if len(args) == 0:
    return ''
    
  ts_args = []
    
  for arg in args:
    ts_type = args[arg]['ts_type']
    ts_args.append(f'{arg}: {ts_type}')
    
  return ', '.join(ts_args)

def make_ts_function(symbol, type_info, args):
  return f"function {symbol}({make_ts_args(args)}): {type_info['ts_type']}" + ' {'
  
def make_ts_api_function_definition(symbol, type_info, args):
  return f"({make_ts_args(args)}) => {type_info['ts_type']}"

def get_arg_groups(symbols, tokens, block_depth):
  tokens = clean_tokens(tokens)
  
  if len(tokens) == 0:
    return []
    
  group_start = 0
  groups = {}
  
  for i in range(len(tokens)):
    if tokens[i] == ',':
      token = tokens[i - 1]
      token_group = tokens[group_start:i - 1]
      groups[token] = get_type_info(symbols, token_group, block_depth)
      group_start = i + 1
      
    if i == len(tokens) - 1:
      token = tokens[len(tokens) - 1]
      token_group = tokens[group_start: len(tokens) - 1]
      groups[token] = get_type_info(symbols, token_group, block_depth)
      
  return groups
    
def process_args(symbols, tokens, block_depth):
  tokens = clean_tokens(tokens)
  arg_groups = get_arg_groups(symbols, tokens, block_depth)
  print('arg groups')
  for group in arg_groups:
    print(group, ':', arg_groups[group])
  
  return arg_groups
  
def process_type(tokens):
  tokens = clean_tokens(tokens)
  print('type:', tokens)
  return tokens[-1]
  
def process_statement(tokens, block_depth, in_struct):
  if block_depth == 0 or in_struct:
    return tokens
    
  #print('process statement placeholder, check for a type definition', tokens)
  assigment_index = find_assignment_index(tokens)
  processed_tokens = []
  
  if assigment_index > -1:
    whitespace = get_starting_whitespace(tokens)
    cleaned_tokens = clean_tokens(tokens[0:assigment_index])
    processed_tokens = [*whitespace, f'let {cleaned_tokens[-1]} ', *tokens[assigment_index:]]
    print('processed tokens are', processed_tokens)
  elif only_symbols_and_whitespace(tokens):
    whitespace = get_starting_whitespace(tokens)
    cleaned_tokens = clean_tokens(tokens[0:])
    if len(cleaned_tokens) > 1:
      print('cleaned tokens are', cleaned_tokens)
      symbol = cleaned_tokens[len(cleaned_tokens) - 2]
      processed_tokens = [*whitespace, f'let {symbol};']
    else:
      processed_tokens = tokens
  else:
    processed_tokens = tokens
    
  return processed_tokens

def clean_tokens(tokens):
  cleaned_list = []
  
  for token in tokens:
    cleaned = token.strip()
    if cleaned != '':
      cleaned_list.append(cleaned)
  
  return cleaned_list

def count_char(string, char_to_find):
  char_count = 0
  
  for char in string:
    if char == char_to_find:
      char_count += 1
      
  return char_count
  
def tokenise(lines):
  tokens = []
  for i in range(len(lines)):
    line = lines[i]
    tokens.extend(tokenise_line(line))
  return tokens

def tokenise_line(string):
  tokens = []
  count = 0
  last_transition = 0
  is_symbol = False
  last_is_symbol = False
  
  while count < len(string):
    char = string[count]
    
    last_is_symbol = is_symbol
    is_symbol = is_symbol_character(char)
    
    if is_newline(char):
      token = string[last_transition:count].strip()
      token and tokens.append(token)
      tokens.append('\n')
      last_transition = count
    elif last_is_symbol:
      if is_symbol != last_is_symbol:
        token = string[last_transition:count].strip()
        token and tokens.append(token)
        last_transition = count
    else:
      token = string[last_transition:count]
      token and tokens.append(token)
      last_transition = count
      
    count += 1
    
  token = string[last_transition:count].strip()
  token and tokens.append(token)
  
  # if tokens == ['\n']:
  #   tokens = []
  
  return tokens

def is_symbol_character(string):
  return bool(re.match('[a-zA-Z0-9_#\.]', string))

def is_newline(string):
  return bool(re.match('[\n\r]', string))
  
def is_whitespace(string):
  return bool(re.match('\s', string))
  
def get_starting_whitespace(tokens): 
  filtered = []
  
  for i in range(len(tokens)):
    if is_whitespace(tokens[i]):
      filtered.append(tokens[i])
      continue
    else:
      break
    
  return filtered
  
def only_symbols_and_whitespace(tokens):
  # skip semicolon
  for i in range(len(tokens) - 1):
    if is_symbol_character(tokens[i]) or is_whitespace(tokens[i]):
      continue
    else:
      return False
    
  return True

def find_open_parenthesis_index(tokens):
  for i in range(len(tokens)):
    if tokens[i] == '(':
      return i
  return -1

def find_close_parenthesis_index(tokens):
  for i in range(len(tokens) - 1, 0, -1):
    if tokens[i] == ')':
      return i
  return -1

def find_assignment_index(tokens):
  in_comment = False
  
  for i in range(len(tokens)):
    if tokens[i] == '/':
      if (i > 0):
        if tokens[i-1] == '/':
          in_comment = True
          
    if tokens[i] == '\n':
      in_comment = False
        
    if not in_comment and tokens[i] == '=':
      if i > 0 and tokens[i-1] == '=':
        continue
      if (i + 1) < len(tokens) and tokens[i+1] == '=':
        continue
      return i
  return -1
  
def get_type_info(symbols, tokens, block_depth):
  if len(tokens) == 0:
    return None

  last = tokens[-1]
  
  if last in symbols:
    return symbols[last]['type_info']
    
  ts_type = last
  if len(ts_type) > 3 and ts_type[0:3] =='vec':
    ts_type = 'Vec' + ts_type[3:]
    
  return {
    'glsl_type': ' '.join(tokens),
    'ts_type': ts_type,
    'block_depth': block_depth
  }
  
