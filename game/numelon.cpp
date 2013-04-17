#include <iostream>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

using namespace std;

int generate_ans(){
  srand((unsigned int)time(NULL));
  return ( (rand()+1) % 10 );
}

int main(){
  int x;
  int y;
  int z;
  
  int ans[3];

  int i = 0;
  char* p;

  cout << "*******Please wait*******" << endl;
  ans[0] = generate_ans();
  sleep(1);
  ans[1] = generate_ans();
  sleep(1);
  ans[2] = generate_ans();
  
  cout << "game start!" << endl;
  
  while(i<=10){
    int flag = 0;

    cout << "一番目の数字を入力して下さい。＞" << endl;
    cin >> x;    
    if(ans[0] == x) flag++;

    cout << "二番目の数字を入力して下さい。＞" << endl;
    cin >> y;
    if(ans[1] == y) flag++;

    cout << "三番目の数字を入力して下さい。＞" << endl;
    cin >> z;
    if(ans[2] == z) flag++;

    if(flag == 3){
      cout << "game set!\n" << "You Win!\n" << endl;
      break;
    }else{
      cout << "This turn is " << flag << " Hits!\nLeast "<< 10-i << "turns.\nnext turn!\n" << endl;
    }
    i++;
  }

  if(i>10) cout << "game set!\n" << "You Lose wwwwwwwwwwwwww!!!\n" << endl;
  cout << "The answer is " << ans[0] << ans[1] << ans[2] << ".\nSee you next game.\n";

  return 0;
}
