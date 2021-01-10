states = reshape(linspace(0,15,16), [4,4]);
V = zeros(4, 4);
theta = 0.001;
gamma = 1;

while 1
    delta = 0;
    for i = 1:4
        for j = 1:4
            if (~((i == 1 && j == 1) || (i == 4 && j == 4)))
                v = V(i,j);
                % v(s) = sum_a pi(s|a) sum_s'r p(s',r|s,a)*[r + gamma*v(s')]
                V(i,j) = -1 + 0.25 * gamma * (V(i,min(j+1, 4)) ...
                                            + V(i,max(j-1, 1)) ...
                                            + V(min(i+1, 4),j) ...
                                            + V(max(i-1, 1),j));
                delta = max(delta, abs(v - V(i, j)));
                V
            end
        end
    end
    
    if (delta < theta)
        break
    end
end