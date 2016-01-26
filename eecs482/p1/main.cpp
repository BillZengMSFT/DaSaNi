#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include "thread.h"

using namespace std;
int max_disk_queue = 0;
int num_of_requesters = 0;
int least_distance = 0;
int queueing_requesters = 0;
int living_requesters = 0;
int current_track = 0;
int current_requester = 0;
vector<int> tracks;
vector<bool> finished;
vector<bool> queueing;
vector<int> indices;
mutex request_mutex;
mutex cout_mutex;
cv service_cv;
cv request_cv;
char ** filenames;
void service(void* a){
	request_mutex.lock();

	while(true){
		while (queueing_requesters < min(max_disk_queue,living_requesters) || living_requesters == 0){
			service_cv.wait(request_mutex);
		}

		int nearest_track = -1;
		int nearest_id = -1;

		int dis = 1000;
		for (unsigned int i = 0;i<tracks.size();i++){
			if (!queueing[i])
				continue;
			else{
				if (abs(current_track - tracks[i]) < dis){
					dis = abs(current_track - tracks[i]);
					nearest_track = tracks[i];
					nearest_id = i;
				}
			}
		}
		if (nearest_track == -1){
			break;
		}
		else{
			current_track = nearest_track;
			cout_mutex.lock();
			cout << "service requester " << nearest_id << " track " << nearest_track << endl;
			cout_mutex.unlock();
			queueing_requesters--;
			queueing[nearest_id] = false;
			request_cv.broadcast();
		}
	}
	request_mutex.unlock();
}




void request(void *i){
	request_mutex.lock();
	int id = *(int *) i;
	ifstream ifs(filenames[id+2]);
	int track;
	while(ifs >> track){
		while (queueing_requesters >= max_disk_queue || queueing[id]){
			service_cv.signal();
			request_cv.wait(request_mutex);
		}
		queueing[id] = true;
		queueing_requesters++;
		tracks[id] = track;
		cout_mutex.lock();
		cout << "requester " << id << " track " << track << endl;
		cout_mutex.unlock();
	}
	service_cv.signal();
	while(queueing[id]){
		request_cv.wait(request_mutex);
	}
	living_requesters--;
	finished[id] = true;
	service_cv.signal();
	request_mutex.unlock();
}



void parent(void *argv){
	for (int i = 0; i < num_of_requesters;i++){
		tracks.push_back(0);
		//cvs.push_back(cv());
		//mutexes.push_back(mutex());
		finished.push_back(false);
		queueing.push_back(false);
	}
	filenames = (char**) argv;
	living_requesters = num_of_requesters;

	for (int i = 0; i < num_of_requesters;i++){
		indices.push_back(i);
	}
	for (int i = 0; i < num_of_requesters;i++){
		thread t((thread_startfunc_t) request,(void *) &indices[i]);
	}
	thread t((thread_startfunc_t) service, (void *) 0);
}

int main(int argc, char* argv[]){
    max_disk_queue = atoi(argv[1]);
    num_of_requesters = argc - 2;
    cpu::boot((thread_startfunc_t) parent, (void *) argv, 0);
}
