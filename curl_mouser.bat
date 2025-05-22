@echo off

@set USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
@set REFERER="https://www.mouser.kr/c/passive-components/capacitors/ceramic-capacitors/?m=Samsung%20Electro-Mechanics&termination%20style=SMD%2FSMT&voltage%20rating%20dc=10%20VDC"
@set MOUSER_URL="https://www.mouser.kr/ProductDetail/Samsung-Electro-Mechanics/CL32Y476KPVVPNE?qs=HoCaDK9Nz5eDPpA1BTvjug%3D%3D"

curl -A %USER_AGENT% ^
     -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9" ^
     -H "Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7" ^
     -H "Connection: keep-alive" ^
     -H "Upgrade-Insecure-Requests: 1" ^
     -H "Sec-Fetch-Dest: document" ^
     -H "Sec-Fetch-Mode: navigate" ^
     -H "Sec-Fetch-Site: none" ^
     -H "Sec-Fetch-User: ?1" ^
     -e %REFERER% ^
     -b "cookies.txt" ^
     %MOUSER_URL% ^
     --output -