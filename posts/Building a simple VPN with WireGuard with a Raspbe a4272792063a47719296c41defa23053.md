# Building a simple VPN with WireGuard with a Raspberry Pi as Server // Andreas Happe

Created: Jan 30, 2020 9:07 AM
Tags: Projects, Tech
URL: https://snikt.net/blog/2020/01/29/building-a-simple-vpn-with-wireguard-with-a-raspberry-pi-as-server/

Now that wireguard will be part of the upcoming Linux 5.6 Kernel it’s time to see how to best integrate it with my [Raspberry Pi based LTE-Router/Access Point Setup](https://snikt.net/blog/2019/06/22/building-an-lte-access-point-with-a-raspberry-pi/).

# What is my scenario?

- Raspberry Pi 3 with a LTE hat, using a public IP address. This will be the VPN server (called *edgewalker* in this post)
- An Android Phone that should use the VPN for all communication when connected
- An Linux Laptop that should use the VPN only accessing network services that are exposed to the VPN

Each device connected to the VPN should be able to connect to all other devices, e.g., my phone should be able to connect to a webserver running on the laptop as long as both are part of the VPN network. If setup is easy enough I’m actually thinking about adding my (Ethernet-connected) Desktop to the VPN too.

Given that wired and wireless connections seem to become more insecure over time ([Tailored Access Operations](https://en.wikipedia.org/wiki/Tailored_Access_Operations), [KRACK attacks against WPA2](https://www.krackattacks.com/) or [Dragonblood attacks against WPA3](https://arstechnica.com/information-technology/2019/04/serious-flaws-leave-wpa3-vulnerable-to-hacks-that-steal-wi-fi-passwords/)) I am seriously considering using wireguard for all my devices, regardless in which environment they are running.

# Installing the Software

WireGuard provides [pre-compiled software packages](https://www.wireguard.com/install/) for most Linux Distributions, Windows and MacOS. Android and iOS applications are provided through the different app stores.

I am using the current Fedora Linux 31 and failed reading the fine manual. I searched for `wireguard-tools` packages, found and installed them. And then was wondering why nothing was working. Further investigation showed that I did not have the `wireguard-dkms` package installed (containing the network driver) and this package was not contained within my distribution repository.

Would I have read the manual I would have done the right steps:

[Untitled](Building%20a%20simple%20VPN%20with%20WireGuard%20with%20a%20Raspbe%20a4272792063a47719296c41defa23053/Untitled%20Database%20d60fe88e71e44732b941d302ac9e9c3f.csv)

On the Raspberry Pi I am using Raspbian Buster, this distribution already included the `wireguard` package, I installed it with:

[Untitled](Building%20a%20simple%20VPN%20with%20WireGuard%20with%20a%20Raspbe%20a4272792063a47719296c41defa23053/Untitled%20Database%2084d4eda03d13471b80045aaef74664fc.csv)

On the Android Phone, I used the Google App Store to install the [WireGuard VPN Application](https://play.google.com/store/apps/details?id=com.wireguard.android).

# Key Setup

Wireguard utilizes a simple private/public key scheme to authenticate VPN peers. You can easily create VPN keys with the following command:

[Untitled](Building%20a%20simple%20VPN%20with%20WireGuard%20with%20a%20Raspbe%20a4272792063a47719296c41defa23053/Untitled%20Database%201cead0efbd0b4811bd8070bae3d68f7f.csv)

This gives us three keypairs (and thus six files at all). We will not refer to those files within the configuration files but copy their content (which is just a single line which is the base64-encoded key) in the configuration files.

# Creating a configuration file for the VPN Server (Raspberry Pi)

Configuration was quite easy, I just created the following file at `/etc/wireguard/wg0.conf`:

[Untitled](Building%20a%20simple%20VPN%20with%20WireGuard%20with%20a%20Raspbe%20a4272792063a47719296c41defa23053/Untitled%20Database%2086ffbe2372fc4cddb21de52e39da3613.csv)

Some notes:

- Please fill in the values from the created key files
- I am creating a VPN network that uses `10.200.200.0/24` for its internal IP range
- my server uses `wwan0` as external network interface in the `PostUp`/`PostDown`-Commands, please adapt that to use your network-facing interface (might be eth0)

It’s easy to bring the VPN network up with the following command:

[Untitled](Building%20a%20simple%20VPN%20with%20WireGuard%20with%20a%20Raspbe%20a4272792063a47719296c41defa23053/Untitled%20Database%209e7f760a758b4f3da348009db1e264ad.csv)

One small thing: I am using `dnsmasq` as DNS server and have bound it to the network interface `br0`. This will be too restrictive for serving DNS requests from connected VPN devices so I added the `wg0` wireguard Ethernet devices to the allowed device list. In dnsmasq you do this by adding a new config line to `/etc/dnsmasq.conf` with the network interface, e.g.:

[Untitled](Building%20a%20simple%20VPN%20with%20WireGuard%20with%20a%20Raspbe%20a4272792063a47719296c41defa23053/Untitled%20Database%20f5595dbeabe74a6e971485162a5c2e4f.csv)

In addition I’ve added some iptable rules to allow traffic to the listening UDP port (51280):

[Untitled](Building%20a%20simple%20VPN%20with%20WireGuard%20with%20a%20Raspbe%20a4272792063a47719296c41defa23053/Untitled%20Database%204579712d7bb14b59a88ae36b27fc8775.csv)

Now that everything works, we can utilize systemd to automatically start the VPN tunnel:

[Untitled](Building%20a%20simple%20VPN%20with%20WireGuard%20with%20a%20Raspbe%20a4272792063a47719296c41defa23053/Untitled%20Database%200b7dbc84ab72443791bc5a0a11274e33.csv)

Mostly the Laptop setup consists of creating a matching configuration file in `/etc/wireguard/wg0.conf` on the Laptop:

[Untitled](Building%20a%20simple%20VPN%20with%20WireGuard%20with%20a%20Raspbe%20a4272792063a47719296c41defa23053/Untitled%20Database%207e45ff8493b34fa1ade1a84ee8e6af77.csv)

Some notes:

- edgewalker should be the public IP-address or public hostname of the VPN server
- By setting `AllowedIPs` to `10.200.200.0/24` we are only using the VPN for accessing the internal VPN network. Traffic to all other IPs/servers will still use the “normal” public internet. Also the pre-configured DNS-Server on the Laptop will be used.

We can use the same `wg-quick` and `systemd` commands for testing as well as for automatic connection setup:

[Untitled](Building%20a%20simple%20VPN%20with%20WireGuard%20with%20a%20Raspbe%20a4272792063a47719296c41defa23053/Untitled%20Database%207b80b1d9c6324faf8e42408ed27aae3b.csv)

We use a very similar configuration file for our Android phone. We prepare the following file (let’s call it `mobile.conf`) on the server through ssh:

[Untitled](Building%20a%20simple%20VPN%20with%20WireGuard%20with%20a%20Raspbe%20a4272792063a47719296c41defa23053/Untitled%20Database%2037e075f9123d4f9088f16fb3a8531955.csv)

In contrast to the laptop setup we are forcing the mobile device to use our VPN server as DNS server (that’s the `DNS` setting) as well as using the newly VPN tunnel for all traffic (by using `0.0.0.0/0` as wildcard for `AllowedIPs`).

It would be tedious to copy this configuration file onto a mobile device, so we convert it into a QR code:

[Untitled](Building%20a%20simple%20VPN%20with%20WireGuard%20with%20a%20Raspbe%20a4272792063a47719296c41defa23053/Untitled%20Database%2039463337e91740079981ae4a2aef5d08.csv)

This outputs an ASCII QR-Code on the console. This code can be scanned from within the Android VPN application and automatically setups the VPN tunnel.

# Conclusion

WireGuard’s configuration is just magic when compared to similar OpenVPN setups..