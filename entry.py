

class Entry:
    """
    Class to store all the entries
    """

    '''
    directory, page, row, year, name, street, number, street_clean, street_only
    '''

    def __init__(self, data: str):
        # split data
        '''
        data = data.split(',')
        if not len(data) == 9:
            print('Data could not be split into appropriate information\n', data)
            'is an error'
            self.invalid = True
        '''
        self.directory, self.page, self.row, self.year, self.name, self.street, self.number, *self.street_opt = data.split(',')

    def __str__(self):
        ref = f'{self.directory}, p{self.page}, r{self.row}'
        return f'Year: {self.year}, Name : {self.name}, Adress: {self.number} {self.street}, Ref: ({ref})'


test = Entry('bpt6k6286466w,378,0,1842,Abadie,Miroménil,21.,Miroménil,Miroménil')
print(test)
