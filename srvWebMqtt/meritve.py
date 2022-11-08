
class Meritve:
    def __init__(self):
        self.labels28 = [
            "čas",
            "skrinja",
            "Dorina soba",
            "Helenina soba",
            "dnevna soba",
            "gretje",
            "zunanja"
        self.labels29 = [
            "čas",
            "soba 001",
            "soba 002",
            "soba 003",
            "RPI",
            "-",
            "zunanja"
        ]
        if myhostname == "malina28":
            self.labels = self.labels28
        else:
            self.labels = self.labels29
        self.reset()


    def reset(self):
        self.time = ""
        self.client_001 = ""
        self.client_002 = ""
        self.client_003 = ""
        self.RPI = ""
        self.RPIa = ""
        self.lj = ""


    def set(self, what, value):
        if False:
            print(what + " " + value)

        if what == "time":
            self.time = value;
        else:
            if isinstance(value, str):
                fv = value
            elif isinstance(value, int):
                fv = str(value)
            elif isinstance(value, float):
                floatVal = float(value)
                fv = "{:.1f}".format(floatVal)
            else:
                fv = ""
            if what == "client_001":
                self.client_001 = fv
            elif what == "client_002":
                self.client_002 = fv
            elif what == "client_003":
                self.client_003 = fv
            elif what == "RPI":
                self.RPI = fv
            elif what == "RPIa":
                self.RPIa = fv
            elif what == "lj":
                self.lj = fv


    def setRow(self, row):
        oneRowOfData = {}
        oneRowOfData['time'] =          str(row[0])
        oneRowOfData['timeLAB'] =       self.labels[0]
        oneRowOfData['client_001'] =    row[3]
        oneRowOfData['client_001LAB'] = self.labels[1]
        oneRowOfData['client_002'] =    row[4]
        oneRowOfData['client_002LAB'] = self.labels[2]
        oneRowOfData['client_003'] =    row[1]
        oneRowOfData['client_003LAB'] = self.labels[3]
        oneRowOfData['RPI'] =           row[2]
        oneRowOfData['RPILAB'] =        self.labels[4]
        oneRowOfData['RPIa'] =          row[5]
        oneRowOfData['RPIaLAB'] =       self.labels[5]
        oneRowOfData['lj'] =            row[6]
        oneRowOfData['ljLAB'] =         self.labels[6]
        oneRowOfData['rangeTime'] =     1

        return oneRowOfData


    def curExecuteCreate(self, cur):
        cur.execute("CREATE TABLE T_data(" +
            "timestamp  DATETIME, " +
            "client_001 REAL, " +
            "client_002 REAL, " +
            "client_003 REAL, " +
            "RPI        REAL, " +
            "RPIa       REAL, " +
            "lj         INTEGER" +
            ")")


    def cursExecuteInsert(self, curs):
        curs.execute("INSERT INTO T_data values(datetime('now','localtime'),(?),(?),(?),(?),(?),(?))",
            (
                self.client_001,
                self.client_002,
                self.client_003,
                self.RPI,
                self.RPIa,
                self.lj
            )
        )


    def cursExecuteSelect(self, curs, numOfSamples):
        return(curs.execute("SELECT "+
            "timestamp, " +
            "client_001,   " +
            "client_002,   " +
            "client_003,   " +
            "RPI," +
            "RPIa,  " +
            "lj " +
            "FROM T_data ORDER BY timestamp DESC LIMIT " + str(numOfSamples)) );


    def printAll(self):
        print("     ",
	self.client_001, ",",
	self.client_002, ",",
	self.client_003, ",",
	self.RPI, ",",
	self.RPIa, ",",
	self.lj)
