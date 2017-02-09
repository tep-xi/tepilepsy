# Importing tepilepsy.widget automatically spawns the background render
# process.  Mac OS is very picky about system calls after fork(), so
# we have to ensure that the thread is started before any widgets are
# imported.  Hence the following line.
import tepilepsy.widget
