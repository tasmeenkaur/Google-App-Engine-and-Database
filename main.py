1.	Main . py 
  
import cgi
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
import csv
import MySQLdb
import os
import jinja2
import time
import logging
import cloudstorage
import cloudstorage as gcs

from google.appengine.api import app_identity
Main_page_html = """\
            <html>
                <body>
                    <form action="/sign" method="post">
                        <h5>Enter the magnitude range :</h5>
                        <div>magnitude 1:<input type = "text" name="m1" rows="1" cols="30"/>
                        magnitude 2:<input type = "text" name="m2" rows="1" cols="30"/></div>
                        <div><input type="submit" value="Submit"></div>
                    </form>
                </body>
            </html>"""

# Configure the Jinja2 environment.
JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  autoescape=True,
  extensions=['jinja2.ext.autoescape'])

# Define your production Cloud SQL instance information.
_INSTANCE_NAME = 'project2-972:assgn2'

class MainPage(webapp2.RequestHandler):

    def get(self):
        
        if (os.getenv('SERVER_SOFTWARE') and   os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):

                    db = MySQLdb.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, db='earthquakes', user='root', charset='utf8', passwd='tas')
                #bucket_name = os.environ.get('BUCKET_NAME', app_identity.get_default_gcs_bucket_name())
                
                
        else:
        
                    db = MySQLdb.connect(host='localhost', port=3306, db='earthquakes', user='root', charset='utf8', passwd='tas')
            
            
        bucket = "/summ/"
        filename = bucket + "allmonth.csv"
            
        gcs_file = cloudstorage.open(filename, 'r')
        fileReader = csv.reader(gcs_file)
        

   
  
        cursor = db.cursor()

            
            
        self.response.out.write(Main_page_html)
        
        db.commit()
        db.close() 

class earthquake(webapp2.RequestHandler):
    def post(self):


        if (os.getenv('SERVER_SOFTWARE') and os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
                    db = MySQLdb.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, db='earthquakes', user='root', charset='utf8', passwd='tas')
        else: 
                    db = MySQLdb.connect(host='localhost', port=3306, db='earthquakes', user='root', charset='utf8', passwd='tas')
        s_time = time.clock()
        cursor = db.cursor()
        cursor.execute("select * from all_month where mag between "+(cgi.escape(self.request.get('m1'))) +" and "+ (cgi.escape(self.request.get('m2')))+ " and time between '2015-05-20T00:00:00Z' and '2015-06-14T23:59:00Z' and type = 'earthquake' ")
        count = cursor.fetchall()
        self.response.out.write("\n No. Of Earthquakes : %d "%len(count))
        e_time = time.clock()
        t_time = e_time - s_time
        self.response.write("time taken to run the query :")
        self.response.write(t_time)
        #self.response.write(m1)
        #b = self.request.get("m2")
        #self.request.get(queries(cursor , self , a ))
        #self.response.out.write('</pre></body></html>')
     

        db.commit()
        db.close()

            #self.redirect("/")

application = webapp2.WSGIApplication([('/', MainPage),
                               ('/sign', earthquake)],
                              debug=True)

def main():
            application = webapp2.WSGIApplication([('/', MainPage),
                                           ('/sign', earthquake)],
                                          debug=True)
            run_wsgi_app(application)

if __name__ == "__main__":
    main()
