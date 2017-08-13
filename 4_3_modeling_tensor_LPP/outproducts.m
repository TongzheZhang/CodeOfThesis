function tens=outproducts(a,b,c)
    len_1=size(a,2);
    len_2=size(b,2);
    len_3=size(c,2);
    for i=1:len_1
        for j=1:len_2
            for k=1:len_3
                tens(i,j,k)=a(i)*b(j)*c(k);
            end
        end
    end
end