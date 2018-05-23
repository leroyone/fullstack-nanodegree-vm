from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databaseSetup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    """docstring for webserverHandler"""
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Hello!"
                output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2>What would you like me to say?</h2><input type="text" name="message" ><input type="submit" value="Submit"></form>'
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "&#161Hola!  <a href = '/hello' >Back to Hello</a>"
                output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2>What would you like me to say?</h2><input type="text" name="message" ><input type="submit" value="Submit"></form>'
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                rests = session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Make a New Restaurant Here</a><br>"
                output += "<p>"
                for eachRest in rests:
                    output += eachRest.name + "<br>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a><br>" % eachRest.id
                    output += "<a href='/restaurants/%s/delete'>Delete</a><br><br>" % eachRest.id
                output += "</p>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1> Make a New Restaurant </h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='newResName' type='text' placeholder='Goobies'>"
                output += "<input type='submit' value='Cdgssgsd'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                resId = int(self.path.split('/')[2])
                resObj = session.query(Restaurant).filter_by(id=resId).one()
                output = ""
                output += "<html><body>"
                output += "<h1>Edit Restaurant Name</h1>"
                output += "<h1> %s </h1>" % resObj.name
                output += "<form method='POST' enctype='multipart/form-data' action='%s'>" % self.path
                output += "<input name='updatedName' type='text' placeholder='New Name'>"
                output += "<input type='submit' value='Update'>"
                output += "</form></body></html>"
                self.wfile.write(output)
                return

            if self.path.endswith("/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                resId = int(self.path.split('/')[2])
                resObj = session.query(Restaurant).filter_by(id=resId).one()
                output = ""
                output += "<html><body>"
                output += "<h1>Are you sure you want to delete '%s' ?</h1>" % resObj.name
                output += "<form method='POST' enctype='multipart/form-data' action='%s'>" % self.path
                output += "<input name='confirmDelete' type='submit' value='Delete'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(output)
                return


        except IOError:
            self.send_error(404, "File Not Found %s" % self.path) 

    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newResName')

                    newRestaurant = Restaurant(name = messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('updatedName')
                    resId = int(self.path.split('/')[2])
                    resObj = session.query(Restaurant).filter_by(id=resId).one()
                    resObj.name = messagecontent[0]
                    session.add(resObj)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/delete"):
                resId = int(self.path.split('/')[2])
                resObj = session.query(Restaurant).filter_by(id=resId).one()
                session.delete(resObj)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()                    
            '''
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output +=  "<html><body>"
            output += " <h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]

            output += '<form method="POST" enctype="multipart/form-data" action="/hello"><h2>What would you like me to say?</h2><input type="text" name="message" ><input type="submit" value="Submit"></form>'
            output += "</body></html>"
            self.wfile.write(output)
            print output
            '''
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()