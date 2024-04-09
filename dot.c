#include <stdio.h>
#include "my_ppmlib.h" /* ppmファイル用ヘッダのインクルード */
#include "label.h"     /* ラベリング用ヘッダのインクルード  */
#include <math.h>
#define DOT_SIZE 5
int main(void)
{
    printf("==== カラーシミュレーター =====\n");
    printf("原画像(ppm(バイナリ)形式)を読み込みます\n");
    load_color_image(0, "\0"); /* ファイル → 画像No.0 への読み込み */
    copy_color_image(0, 1);    /* 画像No.0 → 画像No.1 へコピー     */
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
    // printf("500円玉のみの画像を保存します．\n");
    save_color_image(1, "output.ppm");
}