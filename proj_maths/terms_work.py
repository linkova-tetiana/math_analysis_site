def get_terms_for_table():
    terms = []
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        cnt = 1
        for line in f.readlines()[1:]:
            name, term, definition, source = line.split(";")
            terms.append([name, term, definition])
            cnt += 1
    return terms

def get_test():
    true_results = ['Б', 'А', 'В', 'A']
    result = []
    with open("./data/test.csv", "r", encoding="utf-8") as f:
        inputs = f.readlines()[-1].split(";")
        print(inputs)
        cnt = 0
        for letter in inputs:
            if letter == true_results[cnt]:
                result.append([cnt+1,letter, true_results[cnt], True])
            else:
                result.append([cnt+1,letter,true_results[cnt], False])
            cnt += 1
    return result

def write_term(user_name, new_term, new_definition):
    new_term_line = f"{user_name};{new_term};{new_definition};user"
    with open("./data/terms.csv", "r", encoding="utf-8") as f:
        existing_terms = [l.strip("\n") for l in f.readlines()]
        title = existing_terms[0]
        old_terms = existing_terms[1:]
    terms_sorted = old_terms + [new_term_line]
    new_terms = [title] + terms_sorted
    with open("./data/terms.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(new_terms))
