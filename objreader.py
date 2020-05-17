class ObjReader:
    def __init__(self, filename):
        self.verts = []
        self.norms = []
        self.texes = []
        self.faces = []
        self.facesv = []
        objfile = open(filename, "r")
        for line in objfile.readlines():
            stuff = line.split()
            if stuff.__len__() > 0:
                if stuff[0] == "v":
                    self.verts.append(list(map(float, stuff[1:])))
                if stuff[0] == "vn":
                    self.norms.append(list(map(float, stuff[1:])))
                if stuff[0] == "vt":
                    self.texes.append(list(map(float, stuff[1:])))
                if stuff[0] == "f":
                    self.faces.append(stuff[1:])
                    for i in range(1, stuff.__len__()):
                        stuff[i] = int(stuff[i].split('/')[0]) - 1 #- 1, since obj indeces start from 1, not 0
                    if stuff[1:].__len__() > 3:
                        self.facesv.append(stuff[1:4])
                        self.facesv.append(stuff[2:])
                    else:
                        self.facesv.append(stuff[1:])
    def resize(self, scale):
        for i in range(self.verts.__len__()):
            self.verts[i][0] *= scale
            self.verts[i][1] *= scale
            self.verts[i][2] *= scale