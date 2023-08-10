#include <cstdlib>
#include <string>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
using namespace std;

class Animal;

class World {
private:
  Animal* grid[10][10];
  int count;
public:
  World(int w, int s);
  int run();
  void set(int x, int y, Animal* w);

  //type  1 is w and type 2 is s
  void move(int type);
  void breed(int type);
  void starve(int type);
  Animal* get(int x, int y);
  bool inBound(int x, int y);
  bool sheephere(int x, int y);
  void printb();
};



class Animal {
protected:
  int x, y;
  World* w;
  bool moved;
  int breeding;
  int starving;
public:
  Animal(int x, int y, World* w);
  virtual void move() = 0;
  virtual void breed() = 0;
  virtual void starve() = 0;
  virtual int Type() = 0;
  virtual void kill() {}
};



class Sheep : public Animal {
public:
  Sheep(int x, int y, World* w);
  void move();
  void breed();
  void starve();
  int Type() {return 2;}
  void kill();
};

void Sheep::kill() {
  w->set(x, y, nullptr);
  delete this;
}

class Wolf : public Animal {
public:
  Wolf(int x, int y, World* w);
  void move();
  void breed();
  void starve();
  int Type() {return 1;}
  void kill();
};

void Wolf::kill() {
  w->set(x, y, nullptr);
  delete this;
}

int World::run() {
  bool stop = false;
  while(!stop) {
    int temp = (get(0, 0)!=nullptr?get(0,0)->Type():0);
    move(1);
    //cout<<"1"<<endl;
    move(2);
    //cout<<"2"<<endl;
    starve(1);
    //cout<<"3"<<endl;
    breed(1);
    //cout<<"4"<<endl;
    breed(2);
    //cout<<"5"<<endl;
    stop = true;
    for(int x = 0; x < 10; x++) {
      for(int y = 0; y < 10; y++) {
        if(temp != (get(x, y)!=nullptr?get(x,y)->Type():0))
          stop = false;
      }
    }
    cout<<endl;
    printb();
    count++;
  }
  cout<<"Count "<<count<<endl;
  int temp = (get(0, 0)!=nullptr?get(0,0)->Type():0);
  return temp;
}

void World::move(int type) {
  for(int x = 0; x < 10; x++) {
    for(int y = 0; y < 10; y++) {
      if(grid[x][y] && grid[x][y]->Type()==type) {
        grid[x][y]->move();
      }
    }
  }
}

void World::set(int x, int y, Animal* p) {
  grid[x][y] = p;
}

World::World(int w, int s) {
  count = 0;
  for(int x = 0; x < 10; x++) {
    for(int y = 0; y < 10; y++) {
      grid[x][y] = nullptr;
    }
  }
  //srand(time(NULL));
  for(int i = 0; i < w; i++) {
    bool temp = false;
    int x = rand() % 10;
    int y = rand() % 10;
    while(temp == false) {
      if(grid[x][y]==nullptr) {
        this->set(x, y, new Wolf(x, y, this));
        temp = true;
        //cout<<"placed w"<<endl;
      } else {
        x = rand() % 10;
        y = rand() % 10;
      }
    }
  }
  for(int i = 0; i < s; i++) {
    bool temp = false;
    int x = rand() % 10;
    int y = rand() % 10;
    while(temp == false) {
      if(grid[x][y]==nullptr) {
        this->set(x, y, new Sheep(x, y, this));
        temp = true;
        //cout<<"placed s"<<endl;
      } else {
        x = rand() % 10;
        y = rand() % 10;
      }
    }
  }
}

Animal* World::get(int x, int y) {
  return grid[x][y];
}

bool World::inBound(int x, int y) {
  return((x >= 0 && x <= 9) && (y >= 0 && y <= 9));
}

void World::printb() {
  for(int y = 0; y < 10; y++) {
    for(int x = 0; x < 10; x++) {
      cout<<((grid[x][y]==nullptr)?"-":((grid[x][y]->Type()==1)?"W":"S"))<<" ";
    }
    cout<<endl;
  }
}

Animal::Animal(int x, int y, World* w) {
  this->x = x;
  this->y = y;
  this->w = w;
  moved = false;
}

void Animal::move() {
  //srand(time(NULL));
  //cout<<"WOLF PLS"<<endl;
  int dir = rand() % 4;
  breeding++;
  moved = true;
  if(dir == 0) {//up
    if(w->inBound(x, y-1) && w->get(x,y-1) == nullptr) {
      w->set(x, y, nullptr);
      w->set(x, --y, this);
    }
  } else if(dir == 1) {//right
    if(w->inBound(x+1, y) && w->get(x+1,y) == nullptr) {
      w->set(x, y, nullptr);
      w->set(++x, y, this);
    }
  } else if(dir == 2) {//left
    if(w->inBound(x-1, y) && w->get(x-1,y) == nullptr) {
      w->set(x, y, nullptr);
      w->set(--x, y, this);
    }
  } else if(dir == 3) {//down
    if(w->inBound(x, y+1) && w->get(x,y+1) == nullptr) {
      w->set(x, y, nullptr);
      w->set(x, ++y, this);
    }
  }
}

void World::breed(int type) {
  for(int x = 0; x < 10; x++) {
    for(int y = 0; y < 10; y++) {
      if(grid[x][y] && grid[x][y]->Type()==type) {
        grid[x][y]->breed();
      }
    }
  }
}
void World::starve(int type) {
  for(int x = 0; x < 10; x++) {
    for(int y = 0; y < 10; y++) {
      if(grid[x][y] && grid[x][y]->Type()==type) {
        grid[x][y]->starve();
      }
    }
  }
}

void Sheep::move() {
  //srand(time(NULL));
  int dir = rand() % 4;
  breeding++;
  moved = true;
  if(dir == 0) {//up
    if(w->inBound(x, y-1) && w->get(x,y-1) == nullptr) {
      w->set(x, y, nullptr);
      w->set(x, --y, this);
    }
  } else if(dir == 1) {//right
    if(w->inBound(x+1, y) && w->get(x+1,y) == nullptr) {
      w->set(x, y, nullptr);
      w->set(++x, y, this);
    }
  } else if(dir == 2) {//left
    if(w->inBound(x-1, y) && w->get(x-1,y) == nullptr) {
      w->set(x, y, nullptr);
      w->set(--x, y, this);
    }
  } else if(dir == 3) {//down
    if(w->inBound(x, y+1) && w->get(x,y+1) == nullptr) {
      w->set(x, y, nullptr);
      w->set(x, ++y, this);
    }
  }
}

void Sheep::breed() {
  if(breeding < 3) {
    moved = false;
    return;
  }
  //srand(time(NULL));
  int start = rand() % 4;
  for(int i = 0; i < 4; i++) {
    if(start == 0) {
      if(w->inBound(x, y-1) && w->get(x,y-1) == nullptr) {
        w->set(x, y-1, new Sheep(x, y-1, w));
        breeding = 0;
        return;
      }
    } else if(start == 1) {
      if(w->inBound(x+1, y) && w->get(x+1,y) == nullptr) {
        w->set(x+1, y, new Sheep(x+1, y, w));
        breeding = 0;
        return;
      }
    } else if(start == 2) {
      if(w->inBound(x-1, y) && w->get(x-1,y) == nullptr) {
        w->set(x-1, y, new Sheep(x-1, y, w));
        breeding = 0;
        return;
      }
    } else if(start == 3) {
      if(w->inBound(x, y+1) && w->get(x, y+1) == nullptr) {
        w->set(x, y+1, new Sheep(x, y+1, w));
        breeding = 0;
        return;
      }
    }
    start = (start + 1) % 4;
  }
  moved = false;
}

void Sheep::starve() {
  //cout<<"Error";
}

Sheep::Sheep(int x, int y, World* w):Animal(x, y, w) {
  breeding = 0;
}

Wolf::Wolf(int x, int y, World* w):Animal(x, y, w) {
  breeding = 0;
  starving = 0;
}

void Wolf::breed() {
  if(breeding < 7) {
    moved = false;
    return;
  }
  //srand(time(NULL));
  int start = rand() % 4;
  for(int i = 0; i < 4; i++) {
    if(start == 0) {
      if(w->inBound(x, y-1) && w->get(x,y-1) == nullptr) {
        w->set(x, y-1, new Wolf(x, y-1, w));
        breeding = 0;
        return;
      }
    } else if(start == 1) {
      if(w->inBound(x+1, y) && w->get(x+1,y) == nullptr) {
        w->set(x+1, y, new Wolf(x+1, y, w));
        breeding = 0;
        return;
      }
    } else if(start == 2) {
      if(w->inBound(x-1, y) && w->get(x-1,y) == nullptr) {
        w->set(x-1, y, new Wolf(x-1, y, w));
        breeding = 0;
        return;
      }
    } else if(start == 3) {
      if(w->inBound(x, y+1) && w->get(x, y+1) == nullptr) {
        w->set(x, y+1, new Wolf(x, y+1, w));
        breeding = 0;
        return;
      }
    }
    start = (start + 1) % 4;
  }
  moved = false;
}

void Wolf::starve() {
  if(++starving < 3) {
    moved = false;
    return;
  }
  moved = false;
  kill();
}

void Wolf::move() {
  //cout<<"move"<<endl;
  if(!moved) {
    //cout<<"notmov"<<endl;
    int start = rand() % 4;
    for(int i = 0; i < 4; i++) {
      if(start==0 && w->sheephere(x, y-1)) {//how to say found sheep
        //cout<<"is here"<<endl;
        starving = 0;
        breeding++;
        w->set(x, y, nullptr);
        w->get(x, y-1)->kill();
        w->set(x, --y, this);
        //cout<<"true1"<<endl;
        moved = true;
        i=4;
      } else if (start==1 && w->sheephere(x, y+1)) {
        breeding++;
        starving = 0;
        w->set(x, y, nullptr);
        w->get(x, y+1)->kill();
        w->set(x, ++y, this);
        i=4;
        //cout<<"true2"<<endl;
        moved = true;
      } else if (start == 2 && w->sheephere(x-1, y)) {
        breeding++;
        starving = 0;
        w->set(x, y, nullptr);
        w->get(x-1, y)->kill();
        w->set(--x, y, this);
        i=4;
        //cout<<"true3"<<endl;
        moved = true;
      } else if (start == 3 && w->sheephere(x+1, y)) {
        breeding++;
        starving = 0;
        w->set(x, y, nullptr);
        w->get(x+1, y)->kill();
        w->set(++x, y, this);
        //cout<<"true4"<<endl;
        moved = true;
        i=4;
      }
      start = (start + 1) % 4;
    }
    if(moved==false) {
      //cout<<"here"<<endl;
      Animal::move();
    }
  }
}

bool World::sheephere(int x, int y) {
  if(get(x, y)!=nullptr&&inBound(x,y)) {
    return 2==get(x, y)->Type();
  }
  return false;
}



int main() {
  srand(time(NULL));
  string t;
  double avg = 0;
  //cin>>t;
  //while(t!="q") {
  for(int i = 0; i < 1000; i++) {
    World test(1, 50);
    //test.printb();
    cout<<endl;
    //cout<<"before"<<endl;
    avg += test.run();
    //cout<<"after testrun"<<endl;
    //cin>>t;
  }
  avg = avg/2000;
  cout<<"avg "<<avg;
}
