import turnitin as tii
import personal

cookies = tii.login(personal.email, personal.password)
classes = tii.getClasses(cookies)
print(classes)
