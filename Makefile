compile:
		ln -s freezing-adventure freezing_adventure
		cython freezing_adventure
		gcc -I /usr/include/python2.7/ freezing_adventure.c -lpython2.7 -o freezing_adventure.so -shared -fPIC
		echo "to use compiled version, call ./freezing-adventure as usual"

clean:
		rm freezing_adventure freezing_adventure.so freezing_adventure.c
