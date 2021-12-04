'''
Converts from and to SLCan format.
'''
def is_ack(ch):
  return ch == '\r'

def is_nack(ch):
  return ch == '\a'
# For logging purposes
def format_from_slcan(raw):
  l = len(raw)
  if l == 0:
    print("ERR null string")
    return ""

  is_ext = True if raw[0] in ['T', 'R'] else False
  is_rtr = True if raw[0] in ['R', 'r'] else False

  id = ""
  data_len_i = 4
  if is_ext and l >= 9:
    data_len_i = 9
    id = raw[1:9]
  elif not is_ext and l >= 4:
    id = raw[1:4]
  else:
    print("ERR id len: is_ext [{}] raw str [{}]".format(is_ext, raw))
    return ""

  if data_len_i == l or data_len_i + int(raw[data_len_i]) * 2 >= l:
    print("ERR data len: raw str [{}]".format(raw))
    return ""

  data = ["00"] * 8
  data_st_i = data_len_i + 1
  for i in range(0, int(raw[data_len_i])):
    curr_i = data_st_i + i * 2
    data[i] = raw[curr_i: curr_i + 2]

  # TODO: check for timestamp

  ret = "ID [0x{}] DATA {} RTR [{}] ".format(id, data, int(is_rtr))
  return ret


_head = [['t', 'r'],['T', 'R']]

# To be sent through Serial Line
def convert_to_slcan(id, data, is_ext = False, is_rtr = False):
  ### first char message+id type ###
  msg = _head[is_ext][is_rtr]

  ### id section ###
  if (is_ext and id >= 0x1FFFFFFF) or (not is_ext and id >= 0x7FF):
    print("ERR invalid id: is_ext [{}] id [{}]".format(id))
    return ""
  id_str = hex(id)[2:] # removing 0x
  id_len = 8 if is_ext else 3
  id_str = '0' * (id_len - len(id_str)) + id_str
  msg += id_str

  ### data len ###
  data_len = len(data)
  if data_len == 0 or data_len > 8:
    print("ERR data invalid: {}", data)
    return ""
  msg += str(data_len)

  ### data - array of bytes ###
  for d in data:
    if d > 0xFF:
      print("ERR data invalid: {}", data)
      return
    elem = hex(d)[2:]
    if len(elem) < 2:
      elem = '0' + elem
    msg += elem

  msg += '\r'
  return msg