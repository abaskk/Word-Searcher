
def find_word(row,col,word,grid):
  dirs = [[-1, 0], [1, 0], [1, 1],
          [1, -1], [-1, -1], [-1, 1],
          [0, 1], [0, -1]]
  word_info = {'name':word,'start_coord': None, 
               'end_coord': None,'found':None}
  #print(len(word))
  #found_word = True
  rl = len(grid)
  cl = len(grid[0])
  for x,y in dirs:
    found_word = True
    curr_x = row + x
    curr_y = col + y
    for i in range(1,len(word)):
      #print(curr_x,curr_y)
      if ((0 <= curr_x and curr_x < rl) and
         (0 <= curr_y and curr_y < cl) and
         grid[curr_x][curr_y] == word[i]):
         #print(grid[curr_x][curr_y])
         curr_x += x
         curr_y += y
         #print(found_word)
      else:
        found_word = False
        break
    if found_word == True:
      #print("uuu")
      word_info['start_coord'] = [row,col]
      word_info['end_coord'] = [curr_x-x,curr_y-y] 
      word_info['found'] = True
      break
    else:
      word_info['found'] = False
  
  return word_info
    
def word_search(words,grid):
  word_data = []
  for word in words:
    for row in range(len(grid)):
      for col in range(len(grid[0])):
        if grid[row][col] == word[0]:
          result = find_word(row,col,word,grid)
          if(result['found']):
            #print(result)
            word_data.append(result)
  return word_data



