import yaml
import csv
import requests
import json

####################
## Book Functions ##
####################


def get_book_info(isbn):
    req = f'https://openlibrary.org/isbn/{isbn}.json'
    res = requests.get(req)
    if res.status_code == 200:

        # Creat empty dict to store book info
        book_info = {}

        # Load JSON response text into empty dict
        book_json = json.loads(res.text)

        # Iterate through keys in dict and find needed info
        # Need author info
        # Need title
        for key in book_json:
            if key == 'authors':
                # author_url given as '/authors/OL7855946A'
                # Need to transform into good URL
                # Grab the value at index 0 because some books have
                # multiple authors
                # TODO: write logic for multiple authors
                book_info['author_url'] = 'https://openlibrary.org{}.json'.format(
                    book_json[key][0]['key'])

            # Get title and add to dict
            elif key == 'title':
                book_info['title'] = book_json[key]

    else:
        # TODO: write bad response/error logic
        print('Error!')
    # Return dict with info
    return book_info


def get_author_name(book_info):

    # Grab good author URL from dict and make request
    # URL example: https://openlibrary.org/authors/OL34184A.json
    req = book_info['author_url']
    res = requests.get(req)
    if res.status_code == 200:
        # Return the author name
        return(json.loads(res.text)['name'])
    else:
        # TODO: write bad response/error logic
        print('Error!')


def create_yaml(title, author, rating):

    # TODO: Expand replacement for {"'", ","}
    # Replace spaces with dashes
    review_link = '/projects/books/{}'.format(title.lower().replace(' ', '-'))

    # Return YAML to use for book entry (books.yml) and book review page
    return yaml.dump([{'title': title, 'author': author, 'rating': rating, 'review': review_link}])


def append_book_info(yaml_file, yaml_data):

    # Open books.yml and append book entry
    with open(yaml_file, 'a') as file:
        file.write('\n')
        file.write(yaml_data)


def create_review_file(yaml_data):

    # Load YAML into Python dict
    data = yaml.safe_load(yaml_data)

    # Create the text for front matter
    # TODO: Can we do this directly with YAML?
    text = f"---\nlayout: page\ntitle: {'<em>'+data[0]['title']+'</em> by '+data[0]['author']}\npermalink: {data[0]['review']}\ntags: review book-review\n---\n"

    # Create the file path since it's different
    # than the permalink
    file_path = f"../_books/{data[0]['review'].split('/')[3]}.md"

    # Create file and write front matter to it
    with open(file_path, "w") as file:
        file.write(text)


def add_book(isbn, rating):

    # Get book info from API via ISBN
    book_info = get_book_info(isbn)

    # Pull title
    title = book_info['title']

    # Pull author
    author = get_author_name(book_info)

    # Create actual YAML
    yaml_data = create_yaml(title, author, rating)

    # Use YAML to append entry to books.yml
    append_book_info('../_data/books.yml', yaml_data)

    # Create a new .md file for review and
    # populate with front matter
    create_review_file(yaml_data)


##############################
## Expense Import Functions ##
##############################


def expense_import(csv_file, yaml_file="../_data/spending.yml"):
    csv_file = open(csv_file, 'r')
    yaml_file = open(yaml_file, 'a')
    data = csv.reader(csv_file, delimiter=',', quotechar='"')
    result = list()

    for row_index, row in enumerate(data):
        if row_index == 0:
            data_headings = list()
            for _, heading in enumerate(row):
                data_headings.append(heading)
        else:
            content = dict()
            for cell_index, cell in enumerate(row):
                content[data_headings[cell_index]] = cell
            result.append(content)
    csv_file.close()
    yaml_file.write(yaml.dump(result))
    yaml_file.close()


#######################
## Main Program Loop ##
#######################


while True:
    print("""
  What would you like to do? \n
  1) Import expenses\n
  2) Add new book\n
  3) Add new movie or TV show\n
  Ctrl+C to exit
  """)
    choice = int(input('Choose an option: '))
    if choice == 1:
        csv_name = input(
            'Enter the name of the CSV file (it is assumed to be in the same dir as this script!): ')
        expense_import(csv_name)
        break
    elif choice == 2:
        isbn = input('Enter the ISBN: ')
        rating = input('Enter your rating (out of 5): ')
        add_book(isbn, rating)
        break
    elif choice == 3:
        print('Added new movie/tv show')
        break
    else:
        continue
