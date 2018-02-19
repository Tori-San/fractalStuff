#include<bits/stdc++.h>
using namespace std;

const float eps = 1e-4f;

class vec3 {
    public:
    float x, y, z;

    vec3(float x, float y, float z) : x(x), y(y), z(z) {}

    vec3(){}

    vec3 operator+(const vec3& b) const {
        return {x + b.x, y + b.y, z + b.z};
    }

    vec3 operator-(const vec3& b) const {
        return {x - b.x, y - b.y, z - b.z};
    }

    vec3 operator-() const {
        return {-x, -y, -z};
    }

    float lensqr() const {
        return x * x + y * y + z * z;
    }

    float length() const {
        return sqrt(lensqr());
    }
};

vec3 operator*(float s, const vec3 &a) {
    return {s * a.x, s * a.y, s * a.z};
}

vec3 operator*(const vec3 &a, float s) {
    return s * a;
}

vec3 operator/(const vec3 &a, float s) {
    return {a.x / s, a.y / s, a.z / s};
}

vec3 pow(const vec3 &a, int n) {
    float r = a.length();
    if (r < eps) {
        return {0, 0, 0};
    }
    float phi = atan2(a.y, a.x);
    float theta = acos(a.z / r);

    vec3 b {
        sin(n * theta) * cos(n * phi),
        sin(n * theta) * sin(n * phi),
        cos(n * theta)
    };

    return pow(r, n) * b;
}

ostream& operator<< (ostream& stream, const vec3& a) {
    stream << a.x << " " << a.y << " " << a.z;
    return stream;
}

const int MAX_ITER = 100000;
const int NUM_POINTS = 1000000000;
const int NUM_THREADS = 4;

inline int iterate(vec3 c, vector<vec3> &P) {
    vec3 z = c;
    int i;
    for (i = 0; i < MAX_ITER; ++i) {
        if (z.lensqr() > 4) {
            return i;
        }
        P[i] = z;
        z = pow(z, 8) + c;
    }
    return 0;
}

int main() {

    vector<thread> threads;
    mutex writeLock;
    atomic<uint> amount(0);

    for (int t = 0; t < NUM_THREADS; ++t) {
        threads.emplace_back([&, t](){
            random_device r;
            uniform_real_distribution<float> dist(-2.0f, 2.0f);
            mt19937 gen(r());

            vector<vec3> P (MAX_ITER);
            int i;
            do {
                vec3 c (dist(gen), dist(gen), dist(gen));

                i = iterate(c, P);

                if (i < 15) {
                    i = 0;
                    continue;
                };

                writeLock.lock();
                cerr << "[Thread " << t << "] Writing " << i << " points\n";
                for (int j = 0; j < i; ++j) {
                    cout << c << " " << P[j] << " " << j << "\n";
                }
                writeLock.unlock();
            } while (amount.fetch_add(i) < NUM_POINTS);
        });
    }

    for (auto &t : threads) {
        t.join();
    }
}
