#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#include <linux/i2c.h>
#include <linux/i2c-dev.h>
#include <unistd.h>
#include <sys/time.h>
#include <sys/ioctl.h>

#define I2C_DEV "/dev/i2c-1"

int main(void){

    int tmp75Fd;
    int ret;
    unsigned char slaveAddr = 0x4c;
    unsigned char buf[4] = {0};

    // 打开设备
    tmp75Fd = open(I2C_DEV, O_RDWR);
    if ( tmp75Fd < 0 ){
        printf("faile to open the i2c bus: %s.\n", I2C_DEV);
        return -1;
    }

    // 设置7位地址
    if ( ioctl(tmp75Fd, I2C_TENBIT, 0) < 0) {
        printf("faile to set bits.\n");
        return -1;
    }
    // 强制设置地址
    //if ( ioctl(tmp75Fd, I2C_SLAVE, 0x4c) < 0 ) {
    if ( ioctl(tmp75Fd, I2C_SLAVE_FORCE, 0x4c) < 0 ) {
        perror("faile to set address.\n");
        return -1;
    }

    // 配置tmp75控制器
    buf[0] = 0x01;
    buf[1] =  (1 << 6) | (1 << 5);
    if ( write(tmp75Fd, buf, 2) != 2 ) {
        perror("faile to write config.\n");
        return -1;
    }

    // 读取tmp75控制器中的值，保证配置正确
    buf[0] = 1;
    if ( write(tmp75Fd, buf, 1) != 1 ) {
        perror("faile to write Pointer register.\n");
        return -1;
    }
    buf[0] = 0;
    if ( read(tmp75Fd, buf, 1) != 1 ) {
        perror("faile to read back configure data.\n");
        return -1;
    }
    printf("tmp75 configure: 0x%x.\n", buf[0]);


    // 将tmp75内的寄存器指针指向地址0
    buf[0] = 0;
    if ( write(tmp75Fd, buf, 1) != 1 ) {
        perror("faile to write Pointer register.\n");
        return -1;
    }

    // 循环读取温度数据
    buf[0] = 0;
    buf[1] = 0;
    while ( 1 ) {

        if ( read(tmp75Fd, buf, 2) != 2 ) {
            perror("faile to read data.\n");
            return -1;
        }
        printf("tmp75 temperature: 0x%x%x.\n", buf[0], buf[1]);

        usleep(500000);
    }

    // 貌似是多余的
    close(tmp75Fd);

    return 0;
}
