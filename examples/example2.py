from tables import File, IsRecord

class Particle(IsRecord):
    name        = '16s'  # 16-character String
    lati        = 'i'    # integer
    longi       = 'i'    # integer
    pressure    = 'f'    # float  (single-precision)
    temperature = 'd'    # double (double-precision)

class Event(IsRecord):
    name        = '16s'  # 16-character String
    TDCcount    = 'B'    # unsigned char
    ADCcount    = 'H'    # unsigned short
    xcoord      = 'f'    # float  (single-precision)
    ycoord      = 'f'    # float  (single-precision)

# Open a file in "w"rite mode
fileh = File(name = "example2.h5", mode = "w")
# Get the HDF5 root group
root = fileh.getRootGroup()

# Create the groups:
for groupname in ("Particles", "Events"):
    group = fileh.newGroup(root, groupname)

# Now, create and fill the tables in Particles group
gparticles = fileh.getNode("/Particles")
# You can achieve the same result with the next notation
# (it can be convenient and more intuitive in some contexts)
#gparticles = root.Particles
# Create 3 new tables
for tablename in ("TParticle1", "TParticle2", "TParticle3"):
    # Create a table
    table = fileh.newTable("/Particles", tablename, Particle(),
                           "Particles: "+tablename)
    # Get the record object associated with the table:
    particle = fileh.getRecordObject(table)
    # Fill the table with 10 particles
    for i in xrange(257):
        # First, assign the values to the Particle record
        particle.name  = 'Particle: %6d' % (i)
        particle.lati = i 
        particle.longi = 10 - i
        particle.pressure = float(i*i)
        particle.temperature = float(i**2)
        # This injects the Record values
        fileh.appendRecord(table, particle)      

    # Flush the table buffers
    fileh.flushTable(table)

# Now, go for Events:
for tablename in ("TEvent1", "TEvent2", "TEvent3"):
    # Create a table. Look carefully at how we reference the Events group!.
    table = fileh.newTable(root.Events, tablename, Event(),
                           "Events: "+tablename)
    # Get the record object associated with the table:
    event = table.record
    # Fill the table with 10 events
    for i in xrange(257):
        # First, assign the values to the Event record
        event.name  = 'Event: %6d' % (i)
        event.TDCcount = i % (1<<8)
        # Uncomment the next line to raise a ValueError exception
        #event.TDCcount = i
        event.ADCcount = i * 2
        # Uncomment the next line to raise an AttributeError exception
        #event.xcoor = float(i**2)
        event.xcoord = float(i**2)
        event.ycoord = float(i**4)
        # This injects the Record values
        fileh.appendRecord(table, event)      

    # Flush the buffers
    fileh.flushTable(table)

# Read the records from table "/Events/TEvent3" and select some
e = [ p.TDCcount for p in fileh.readRecords("/Events/TEvent3")
      if p.ADCcount < 20 and 4<= p.TDCcount < 15 ]
print "Last record ==>", p
print "Selected values ==>", e
print "Total selected records ==> ", len(e)

# Finally, close the file (this also will flush all the remaining buffers!)
fileh.close()

