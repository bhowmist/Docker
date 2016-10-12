#!/usr/bin/python
#Given a string this program returns the longest substring in alphabetical order#

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import json
import urlparse
import sys

PORT_NUMBER = 80           

def alpha(s):
       
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
           return "Longest substring in alphabetical order is:" +" " +alpha_store
      else :
           return "Longest substring in alphabetical order is:" +" " +alphafinal_store   

  
#This class will handles any incoming request from the browser
class myHandler(BaseHTTPRequestHandler):

	#Handler for the GET requests
  def do_GET(self):
    if self.path.startswith("/alpha"):
      o = urlparse.urlparse(self.path)
      getvars = urlparse.parse_qs(o.query)
      try:
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        s = str( getvars['s'][0] )
        
        self.wfile.write( json.dumps( alpha(s)) )
        return
      except:
        e = sys.exc_info()[0]
        self.send_error(404,'Error, provide a and b parameters' + str(e) + str(getvars.keys()))
        return
    self.send_error(404,'Resource Not Found')

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
