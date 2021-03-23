import wda

# 如果只有一个设备也可以简写为
# If there is only one iPhone connecttd
c = wda.USBClient()

# 支持指定设备的udid，和WDA的端口号
# Specify udid and WDA port
c = wda.USBClient("184ed2e8e26199478f1e7c70605121c457877165", port=8100)
print (c.status())

# Wait WDA ready
c.wait_ready(timeout=300) # 等待300s，默认120s


# Press home button
c.home()

# Hit healthcheck
c.healthcheck()

c.screenshot().save("screen.jpg") # Good


with c.session('com.apple.Health') as s:
	print(s.orientation)
	

c.wait_ready(timeout=20)	
s = c.session('com.apple.mobilesafari', ['-u', 'https://www.google.com/ncr'])
print(s.orientation)
s.close()