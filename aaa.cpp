
#include<bits/stdc++.h> using namespace std;
#define int long long
#define rep(i, n) for (int i = 0; i < (n); i++) #define all(x) x.begin(), x.end()
#define pb push_back
#define fi first
#define se second
main(){
ios::sync_with_stdio (false); cin. tie(0), cout.tie(0);
int n,k; cin>>n>>k; int ar[n]; rep(i,n){
}
cin>>ar[i];
int t[n]; rep(i,n){
}
cin>>t[i];
int mx = 0, h = 0;
for (int i = 0; i < n;i++){
int sum = 0;
if(t[i] == 0){
for(int j = i;j <= i+k;j++){
if(t[i] == 0){
sum = sum + ar[i];
}
}
if(mx < sum) {
mx = sum;
h = i;
}
}
}
int sum = 0;
for(int i = h;i < h+k; i++){
t[i] = 1;
}
rep(i,n){
if(t[i] == 1) {
sum += ar[i];
}
}
cout<<sum;
}