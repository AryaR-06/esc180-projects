import math
def norm(vec):
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)

def cosine_similarity(vec1, vec2):
    for key in vec1:
        if key not in vec2:
            vec2[key] = 0

    for key in vec2:
        if key not in vec1:
            vec1[key] = 0

    sum = 0
    for key in vec1:
        sum += vec1[key]*vec2[key]

    return sum/(norm(vec1)*norm(vec2))

def build_semantic_descriptors(sentences):
    d = {}
    for sentence in sentences:
        for word in sentence:
            if word not in d:
                d[word] = {}

    for sentence in sentences:
        unique_words = set(sentence)
        for dict_word in unique_words:
            for cur_word in unique_words:   
                if dict_word != cur_word:
                    if cur_word not in d[dict_word]:
                        d[dict_word][cur_word] = 1
                    else:
                        d[dict_word][cur_word] += 1
    return d      

def build_semantic_descriptors_from_files(filenames):
    sentences = []
    for i in range (len(filenames)):
        with open(filenames[i], 'r', encoding='utf-8') as f:
            words = f.read().split()
            last_split = 0
            for i in range (len(words)):
                for sep in [".", "!", "?"]:
                    if sep in words[i]:
                        sentences.append (words[last_split:i+1])
                        last_split = i+1
    for i in range (len(sentences)):
        for j in range (len(sentences[i])):
            for sep in [".", "!", "?", ",", "-", "--", ":", ";"]:
                if sep in sentences[i][j]:
                    if sep == "-" or sep == "--":
                        sentences[i][j] = sentences[i][j].replace(sep, " ")                      
                    else:
                        sentences[i][j] = sentences[i][j].replace(sep, "")
            sentences[i][j] = sentences[i][j].lower()
            if sentences[i][j] == "":
                sentences[i].pop(j)
    d = build_semantic_descriptors (sentences)
    return d      

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    choices_match = {}
    for choice in choices:
        if choice not in choices_match:
            if (choice in semantic_descriptors) and (word in semantic_descriptors):
                choices_match[choice] = similarity_fn (semantic_descriptors[word], semantic_descriptors[choice])
            else:
                choices_match[choice] = -1

    most_score = max (choices_match.values())
    for key in choices_match:
        if choices_match[key] == most_score:
            return key
 
def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    total = 0
    correct = 0
    with open (filename, "r", encoding='utf-8') as f:
        for line in f:
            words = line.strip().split()
            fn_ans = most_similar_word (words[0], words[2:], semantic_descriptors, similarity_fn)
            actual_ans = words[1]
            if fn_ans == actual_ans:
                correct += 1
            total += 1
    return 100*(correct/total)