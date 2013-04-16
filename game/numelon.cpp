#include <iostream>
#include <string>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

using namespace std;

char generate_ans(){
  srand((unsigned int)time(NULL));
  return ( (rand()+1) % 10 );
}

int main(){
  char x;
  char y;
  char z;
  
  char ans_x[5];
  char ans_y[5];
  char ans_z[5];
  
  sprintf(ans_x,"%d",generate_ans());
  
  cout << "game start!" << endl;
  cout << "一番目の数字を入力して下さい。＞" << endl;
  cin >> x;
  cout << "二番目の数字を入力して下さい。＞" << endl;
  cin >> y;
  cout << "三番目の数字を入力して下さい。＞" << endl;
  cin >> z;

  cout << ans_x << endl;

  return 0;
}
