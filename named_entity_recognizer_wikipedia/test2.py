import sys 

def main(sys.argv):
    
    f = open('document.pos', 'w+')
    f.write(sys.argv[1])
    f.close()
    
    
if __name__ == "__main__":
    main(argv)