EXEC = uart_test
OBJS = uart_test.o

TARGET_CC = arm-linux-gnueabihf-gcc
CC = ${TARGET_CC}


all:${EXEC}
${EXEC} : ${OBJS}
	${CC} ${CFLAGS} ${LDFLAGS} -o $@ ${OBJS} 
${OBJS2} : ${HEADERS}

.PHONY : clean
clean :
	-rm -f ${OBJS} ${EXEC}
