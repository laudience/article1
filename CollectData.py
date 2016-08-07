from utilitaires import *

api = get_API()



def main():
    save_list(api, 'AssembleeNat', 'les-deputes', 'data.csv')


if __name__ == '__main__':
    main()