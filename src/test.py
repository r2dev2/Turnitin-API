import turnitin as tii
import personal

cookies = tii.login(personal.email, personal.password)
classes = tii.getClasses(cookies)
for classroom in classes:
    print(classroom["title"] + ": " + classroom["url"])
assignments = tii.getAssignments(classes[0]["url"], cookies)
for assignment in assignments:
    print(assignment["title"] + ": " + str(assignment["dates"]))
