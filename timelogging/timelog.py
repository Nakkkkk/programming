class FileMNG:

  def __init__(self):
    self.readlines = ''

  def filewrite(self,filenameW,sent):
    fw = open(filenameW,'w')
    fw.write(sent)
    fw.close()

  def fileread(self,filenameR):
    fr = open(filenameR,'r')
    self.readlines = fr.readlines()
    fr.close()

if __name__ == '__main__':

  a = FileMNG()

  print 'write'
  sent = 'testtest aaaaaaaa'
  a.filewrite('testtest.txt',sent)

  print 'read'
  a.fileread('testtest.txt')
  print str(a.readlines) + 'bbbbbbbbb'
