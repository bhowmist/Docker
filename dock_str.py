#!/usr/bin/python

#text analysis

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import json
import urlparse
import sys

PORT_NUMBER = 8080 
          
#character count
def CharCount(a):
  k = len(a)
  return k

#space count
def SpaceCount(a):
  k = a.count(' ')
  return k

#uppercase letter count
def UpperCount(a):
  k = sum(1 for c in a if c.isupper())
  return k

#lowercase letter count
def LowerCount(a):
  k = sum(1 for c in a if c.islower())
  return k 

#special character count
def Special(text):
     num=0
     spec=0
     for i in text:
         if ord(i)>=48 and ord(i)<=57:
              num+=1
         elif (ord(i)>=65 and ord(i)<=90) or (ord(i)>=97 and ord(i)<=122) or (i==' '):
              pass
         else:
              spec+=1
     return (num, spec)

#longest substring calculation
def sub(s):
      count=0
      count_final=0
      alpha_store=" "
      alphafinal_store=" "
      init=0
      for char in s:
            if init<=char :
                count+=1
                alpha_store=alpha_store + char 
            elif (count>count_final):
                 count_final=count
                 alphafinal_store=alpha_store
                 alpha_store=char
                 count=1
            else:
                count=1
                alpha_store=char
            init=char
      if count>count_final :         
           return (s,alpha_store)
      else :
           return (s,alphafinal_store) 

#word count
def WordCount(text):
     text=text.strip()
     text=text.split()
     d={}
     for word in text:
          if d.get(word)==None:
                d[word]=1
          else:
                d[word]+=1
     return d
     
  
#This class will handles any incoming request from the browser
class myHandler(BaseHTTPRequestHandler):

  #Handler for the GET requests
  def do_GET(self):
    if self.path.startswith("/text"):
      o = urlparse.urlparse(self.path)
      getvars = urlparse.parse_qs(o.query)
      try:
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        data = str( getvars['data'][0] )
        self.wfile.write( 'Input string is :')
        self.wfile.write( json.dumps( sub(data)[0]) )
        self.wfile.write( '\n')
        self.wfile.write( 'Number of characters in the string:')
        self.wfile.write( json.dumps( CharCount(data)) )
        self.wfile.write( '\n')
        self.wfile.write( 'Number of spaces in the string:')
        self.wfile.write( json.dumps( SpaceCount(data)) )
        self.wfile.write( '\n')
        self.wfile.write( 'Number of uppercase letters in the string:')
        self.wfile.write( json.dumps( UpperCount(data)) )
        self.wfile.write( '\n')
        self.wfile.write( 'Number of lowercase letters in the string:')
        self.wfile.write( json.dumps( LowerCount(data)) )
        self.wfile.write( '\n')
        self.wfile.write( 'Number of digits in the string:')
        self.wfile.write( json.dumps( Special(data)[0]) )
        self.wfile.write( '\n')
        self.wfile.write( 'Number of special characters in the string:')
        self.wfile.write( json.dumps( Special(data)[1]) )
        self.wfile.write( '\n')
        self.wfile.write( 'Longest substring in alphabetical order is:')
        self.wfile.write( json.dumps( sub(data)[1]) )
        self.wfile.write( '\n')
        self.wfile.write( 'Word Count is as follows:\n')
        count=WordCount(data)
        for k in count:
             self.wfile.write( json.dumps(k) )
             self.wfile.write( ':')
             self.wfile.write( json.dumps(count[k]) )
             self.wfile.write( '\n')
        return
      except:
        e = sys.exc_info()[0]
        self.send_error(404,'Error, provide a and b parameters' + str(e) + str(getvars.keys()))
        return
    self.send_error(404,'Resource Not Found')


#driver code 
if __name__ == "__main__":
  try:
	  #Create a web server and define the handler to manage the
	  #incoming request
	  server = HTTPServer(('', PORT_NUMBER), myHandler)
	  print 'Started httpserver on port ' , PORT_NUMBER

	  #Wait forever for incoming http requests
	  server.serve_forever()

  except KeyboardInterrupt:
	  print '^C received, shutting down the web server'
	  server.socket.close()
