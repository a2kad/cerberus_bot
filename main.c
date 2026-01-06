#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <linux/if_packet.h>
#include <net/ethernet.h>
#include <netinet/in.h>
#include <endian.h>

struct ip_header {

#if __BYTE_ORDER == __LITTLE_ENDIAN
	uint8_t		ihl:4;
	uint8_t		version:4;
#elif __BYTE_ORDER == __BIG_ENDIAN
	uint8_t		version:4;
	uint8_t		ilh:4;
#else
	#error "Unknown endianness"
#endif

	uint8_t		tos;
	uint16_t	total_length;
	uint16_t	id;
	uint16_t	frag_offset;
	uint8_t		ttl;
	uint8_t		protocol;
	uint16_t	checksum;
	uint32_t	src_addr;
	uint32_t	dest_addr;
}__attribute__((packed));

void	print_ip_packats(const unsigned char *buffer) {
	const struct ip_header *ip = (const struct ip_header *)buffer;

	struct in_addr src, dst;
	src.s_addr = ip->src_addr;
	dst.s_addr = ip->dest_addr;

	printf("IPv%u\nIHL: %u\nTotal Length: %u\nProtocol: %u\n %s -> %s\n",
			ip->version,
			ip->ihl,
			ntohs(ip->total_length),
			ip->protocol,
			inet_ntoa(src),
			inet_ntoa(dst)
		 );
}

int main(void){
	int raw_sock;
	struct sockaddr_ll sll;
	unsigned char buffer[65536];

	raw_sock = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
	if (raw_sock < 0){
		perror("Socket Error (Are you root?)");
		return 1;
	}

	while (1)
	{
		socklen_t sll_len = sizeof(sll);

		int data_size = recvfrom(raw_sock, buffer, 65536, 0, (struct sockaddr *)&sll, &sll_len);
		if (data_size < 0){
			perror("Recvfrom error");
			return 1;
		}

		struct ethhdr *eth = (struct ethhdr *)buffer;
		if (ntohs(eth->h_proto) == ETH_P_IP){
			print_ip_packats(buffer + sizeof(struct ethhdr));
		}
	}

	close(raw_sock);
	return 0;
}