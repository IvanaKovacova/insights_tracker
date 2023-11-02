FILEPATH = 'files/projectlist.txt'

def get_projects(filepath=FILEPATH):
    with open(filepath, 'r') as file:
        projects = file.readlines()
        return projects

