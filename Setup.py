import pickle

files = ["categories.txt", "recipients_alias.txt", "alias.txt", "alias_category.txt"]
path = "C:\\Users\\Manya Sharma\\Desktop\\data science flask\\"
with open(path + "categories_reset.txt", 'rb') as f:
    categories = pickle.load(f)
rec_alias = dict()
alias = dict()
alias_cat = dict()
transactions = dict()
category_list = ["Food",
                 "Online",
                 "Travel",
                 "Medical",
                 "Friends",
                 "General",
                 "Academic",
                 "Entertainment",
                 "Other"]

def setup():
    global files
    _all_dict = []
    for file in files:
        with open(path + file, 'rb') as ff:
            _all_dict.append(pickle.load(ff))
    return _all_dict

def run(rec_list: list, categories: dict, rec_alias: dict, alias: dict, alias_cat:dict):

    for rec in rec_list:
        if rec not in rec_alias:
            print(f"Unknown category for {rec}")
            _alias = input(f"Enter alias for {rec}. Press enter to skip: ")
            _alias = _alias if _alias else rec
            print(_alias)
            rec_alias[rec] = _alias

            try:
                alias[_alias].append(rec)
            except:
                print(f'''New alias found! {_alias}
Category List:''')

                for i in range(len(category_list)):
                    print(f"{category_list[i]} -> {i + 1}")

                _category = input(f"Enter category for {_alias}. Press enter to skip: ")
                _category = int(_category)-1 if _category else 8
                alias[_alias] = [rec]
                alias_cat[_alias] = category_list[_category]
                categories[category_list[_category]].append(_alias)
        else:
            print(f"{rec} found in category {alias_cat[rec_alias[rec]]}!")
        
    return categories, rec_alias, alias, alias_cat

def reset():
    with open(path + "categories_reset.txt", 'rb') as f:
        categories = pickle.load(f)
    
    return categories, dict(), dict(), dict(), dict()


def finishRun(categories: dict, rec_alias: dict, alias: dict, alias_cat: dict):
    global files
    _all_dict = [categories, rec_alias, alias, alias_cat]
    for i in range(4):
        with open(files[i], 'wb') as file:
            pickle.dump(_all_dict[i], file)