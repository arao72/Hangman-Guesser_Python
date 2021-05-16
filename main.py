from collections import defaultdict

from hangmen import HANGMEN

AVOID_WRONG_WEIGHT = 1
TOTAL_WRONG_GUESSES = len(HANGMEN)

def get_freq(pt):
  return sum(word[1] for word in pt)

def get_avg_remaining(pt):
  return len(pt) * get_freq(pt)

def word_score(pts):
  avg_left = 0
  for pt in pts.values():
    avg_left += get_avg_remaining(pt)
  return avg_left + AVOID_WRONG_WEIGHT * get_freq(pts[()])

def get_pos(word, letter):
  return tuple(ind for ind, char in enumerate(word) if char == letter)

def partition_poses(words, letter):
  res = defaultdict(list)
  for word in words:
    res[get_pos(word[0], letter)].append(word)
  return res

def get_best_letter(words, letters):
  half_len = len(words) // 2
  best_score = float('inf')
  best_letter = None
  best_partition = None
  for letter in letters:
    partitions = partition_poses(words, letter)
    score = word_score(partitions)
    if score < best_score:
      best_score = score
      best_letter = letter
      best_partition = partitions
  return best_letter, best_partition

print(f"Loading database...")

orig_words = [word.strip().split("\t") for word in open("words").readlines()]
orig_words = [(word[0], float(word[1])) for word in orig_words]
orig_words_dict = defaultdict(list)
for word in orig_words:
  orig_words_dict[len(word[0])].append(word) # partition by word length
  
print(f"Loaded {len(orig_words)} word database.")
print()

print(__doc__)
input("Press enter to start")

while True:
  wrong_guesses = 0
  
  letters = set("abcdefghijklmnopqrstuvwxyz")
  
  length = int(input("How long is the word?"))
  
  words = orig_words_dict[length]
  
  if not words:
    print("I don't know any words that long")
    break
  
  while len(words) > 1:
    best_letter, partition = get_best_letter(words, letters)
    letters.remove(best_letter)
    pos = input(f"Where does the letter '{best_letter}' appear? ").replace(" ", "")
    if not pos:
      pos = ()
      print(HANGMEN[wrong_guesses])
      wrong_guesses += 1
      if wrong_guesses == TOTAL_WRONG_GUESSES:
        print("I would have won, if not for you meddling kids!")
        break
    else:
      pos = tuple([int(num) - 1 for num in pos.split(",")])
    if pos not in partition:
      print("Your word is not in my database")
      break
    words = partition[pos]
  else: # if not broken
    if input(f"Is the word {words[0][0]}? [y/n]").lower() == "y":
      print("I win!")
    else:
      print("Your word is not in my database")
    print()