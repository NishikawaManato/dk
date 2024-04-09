#include <stdio.h>
#include "my_ppmlib.h" /* ppm�t�@�C���p�w�b�_�̃C���N���[�h */
#include "label.h"     /* ���x�����O�p�w�b�_�̃C���N���[�h  */
#include <math.h>
#define DOT_SIZE 5
int main(void)
{
    printf("==== �J���[�V�~�����[�^�[ =====\n");
    printf("���摜(ppm(�o�C�i��)�`��)��ǂݍ��݂܂�\n");
    load_color_image(0, "\0"); /* �t�@�C�� �� �摜No.0 �ւ̓ǂݍ��� */
    copy_color_image(0, 1);    /* �摜No.0 �� �摜No.1 �փR�s�[     */
    int x, y, col, tent;
    int max[3] = {0, 0, 0}, min[3] = {MAX_BRIGHTNESS, MAX_BRIGHTNESS, MAX_BRIGHTNESS};
    for (y = 0; y < height[1] - 1; y += DOT_SIZE)
    {
        for (x = 0; x < width[1] - 1; x += DOT_SIZE)
        {
            for (col = 0; col < 3; col++)
            {
            }
        }
    }

    for (y = 0; y < height[1] - 1; y += DOT_SIZE)
    {
        for (x = 0; x < width[1] - 1; x += DOT_SIZE)
        {
            for (col = 0; col < 3; col++)
            {

                tent = 0;
                for (int i = 0; i < DOT_SIZE; i++)
                {
                    for (int j = 0; j < DOT_SIZE; j++)
                    {
                        tent += image[0][x + i][y + j][col];
                    }
                }

                for (int i = 0; i < DOT_SIZE; i++)
                {
                    for (int j = 0; j < DOT_SIZE; j++)
                    {
                        image[1][x + i][y + j][col] = tent / pow(DOT_SIZE, 2);
                    }
                }
            }
        }
    }
/*
    for (col = 0; col < 3; col++)
    {
        for (y = 0; y < height[1] - 1; y++)
        {
            for (x = 0; x < width[1] - 1; x++)
            {

                if (max[col] < image[1][x][y][col])
                    max[col] = image[1][x][y][col];
                if (min[col] > image[1][x][y][col])
                    min[col] = image[1][x][y][col];
            }
        }
        printf("%d,%d\n", max[col], min[col]);
    }
    for (y = 0; y < height[1] - 1; y++)
    {
        for (x = 0; x < width[1] - 1; x++)
        {
            for (col = 0; col < 3; col++)
            {
                if (image[1][x][y][col] < (max[col] - min[col] + 3 * min[col]) / 3)
                {
                    image[1][x][y][col] = (max[col] - min[col] + 3 * min[col]) / 3;
                }
                else if (image[1][x][y][col] < (2 * max[col] - 2 * min[col] + 3 * min[col]) / 3)
                {
                    image[1][x][y][col] = (2 * max[col] - 2 * min[col] + 3 * min[col]) / 3;
                }
                else
                {
                    image[1][x][y][col] = max[col];
                }
            }
        }
    }
*/
    // printf("500�~�ʂ݂̂̉摜��ۑ����܂��D\n");
    save_color_image(1, "output.ppm");
}