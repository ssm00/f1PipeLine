import requests


"""
https://www.pinterest.co.kr/resource/BaseSearchResource/get/?source_url=/search/pins/?q=charles%20leclerc&rs=typed&data={"options":{"applied_filters":null,"appliedProductFilters":"---","article":null,"auto_correction_disabled":false,"corpus":null,"customized_rerank_type":null,"domains":null,"filters":null,"first_page_size":null,"page_size":null,"price_max":null,"price_min":null,"query_pin_sigs":null,"query":"charles leclerc","redux_normalize_feed":true,"rs":"typed","scope":"pins","source_id":null,"top_pin_id":null},"context":{}}&_=1714935308824"""


header = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'cookie': f'csrftoken=36965480027b268da1264bbd2aeb63b0; g_state={"i_l":0}; _auth=1; cm_sub=none; ar_debug=1; _routing_id="7d5cf6ad-02eb-46dd-97a3-8786200a7b3e"; sessionFunnelEventLogged=1; _pinterest_sess=TWc9PSZZT1FwTVp6UU53NVVQc05SS3A0U1dYdlV0ZzdWSmt1UTZibnlYdHRYa3h2N3FzQytxd0d1TktuSHRpVDNtVDdoQmlvejhnMUdNZXpnVGtFaExqVzJUcVlGN3FSYVNsWnczSHk2N29rSlVWT2ZPeTBMa2FGS0svUlRsWG0rU05kdjdnTld5cjhVSzF4d2pVNFpGRGlGcEpQblZibzd6a2t1cFpPY0daQWNHaGpIdnNIemdNaXVrMmFGU0VNS1lLenBuTHFCaGxYZjlhaGJUTHNaT0VnUTF6R3NET1pyZTVhWGJ6Nm5ESS8rMTlvUGdYemt1ZHEwS1ppQTBDcWQ0QmJVdldlMHlLeTNrRzhDRFJERk5MMEhIb25UQUMxbkVuNklnYzRIdEUwekJNRm1YRkZhZE0yWVNYOU40ekFEUHlXZVRUM1pMOUl5dkdqdnFnN0hkcDlFcXBGTGhZWEFoSXd1bkIxOHBjTytwank1M2Z0OExFUkV5U0hCOGpUOHpLVHdTdS9aczdNMUxQMFA4Sys3SmUycVhnUkx1TUZ5SEovVnJGMSswVmJUTG82cno3ZXpINnZvVTMyR2pUZVY5SnlxK3R4K3g5V0NSZ3ZoQXhZSU5vSHM3dCtKalBLd3ZjTVRCKzVPWEpJZGxoa0NRZ0tHYkFnblBBVVpSUnh3WUpPajBCT3ZzVnhjZmZZUVBwOXFYSjVaNHgwU29qQUkrZkRxM1VMRC9hR09NbEt6aS9aSU5SUThYUFdQRUVLMVA4WHJaWDFNRFVQS09ZWVpOYjl1N0dUdDRESUxucW9jQS9yT3Y0L25MS2JSRWsrSXBrSTgxbkFrZmtESDFmcmkrZUZsMktjbUY2MytlWVJmNWkzcjB5TlRDc1Rjd21rTmtaVUQ3czlSdFFPbUUwNURpa2JUTTVPMW40eEU5RDNGS2pRbExxSjEwV2wwaWZhQnNFZjhqQmlqdmFoUEZxVnpTWDYrSE94ckpWMXNzVnYvSjhOWlFaeEdOTloyaGVmdFFGTE9qWGg3QjlNN1NHYXF4ckVqUjZSV2kvaUFwc1ZZOEIzK0RsenEyYVNmR0pXQ3MrNUVVTVg3dXNTWTQrNmxyYSs3RFlaUXJCaG8rU1lncVJucnF2Vk9GSERWcGV4dktEL2xUUTZSaTV0Wm92MXk4YUpyTkpGa1krQzJkOUhWVXNtNW5SN3p5SlBmZEwzcFZJZHN0aDA2N0hmMFJRT1JkMzJnd215SFVoRHBvaUhvdVBELzh5MVNmOXl2NXlId0tjUmxEMmtheVlweU4rVWZoTTl5aGJ6UFhkNk1FbE8vYUJTWFJSR3BjZWFXMmJ4cnZOd3VLRDlYcWtvNzhnRW1icitmeXNnZXUxOGR3SGxjNkVmbTRmSnp6L201a2NBdnF1WXBZQi9MZ0VpR3p3RVEvRXRwTTcraXZUYkZRZGQvM05HcENsYVQwZUdFU3M1bTVqVCtSSUprZWhvS013YkNhVUpqTlRnQ28xamtlb3N1Ujdsc1pVNkk3MWd4V29QbHZydUtlWmtaejBYeUtNOUdadEJMa2hrdDlzbE1GRWJIdHhTR1pVRVUzakZRRXh5Wko5ZGVPRzN6bTM4eE0xRHE5clVkMCtjVkw5QzBGbHlyRnQ0ZUJ5Vm0rWHNIWHlJcG1qMVFKR2dEeTI5YVRWMFJDUlJrY0dJem9oZkZsVUVtVXE4b2NoUU5wYjV0VHJYYzRtT0Nmc3YvYmpsclRkdEJZYUpSM3RGQ2lCQjIzVnFmamEyNzlCNVVMY0lmekQ2eXQ4RTkmeHh6TXFiQ21LN3p5RHZQNUQreWVXekV3cEJZPQ==; __Secure-s_a=VXpDeTJYYVYvb2pZN3NxTVJna3BvWWU3amQwdjJ6bmxxdkJqTWRPQnRmTHdEeCtjT3VnSjJKaGVQTHFjTGpMMjMwQ040dVJZNmtqQ0xNcW9WbFBSaXVNbGFvU3NmeW5OenFpMWg0eHJmaEVzTHh1aXVEYlRFUXBxMHFiOUllVlVVbW51NVNDc3RId0I0bzF6bCtWbVY3bGRyMFQxZENMVVYwRm1BVlRXcTNaRWlRaXc0RFQrNlRBR2txcWtDWnhpbDJaR29ac0xlc0ZCK3JJNWpyYUczYzRIM1BVUEIyeUFwSGNYalZzYmR3dFNmZnlRMFpIUXJUaUVVSnhHWUc5MDg3NjYxajNZckV1Z3BxWk4zb1k0Y1czYithNjZiM0NUeE5NZ3hNS3Mrd0NLOGp2RkZpc2hDVjFXVHNzMFFRQ2lqSUF6Qjk4bzliU2w2N3NoMzlRTVVpVE45UnBkNG9TMzZwcUhnWHM2VmZpNkhOMDJnSjBaeW85dVgwQW9yRU9UYlpKcHBlZFkvU2UyUFltNjQzTk9DM1ZWVUliVG9FNDQ3Vnh5a21qN1puQllVeTMxWGV1eEpkOTdLbkMzcWpHNHBtMzNYTWcyamFHbWtXNmNnak1CZGFKUHpMZ3VaV2wwMTcxdFYvRHpFOGQydmdkNFVuUnJqUzIraGZneDJOWHZ6WUI5Y2V4VXR1RmFNSnhId1RVNU4zdmdZcHlaTGRCOWxJOUJTMHg2YldKSEhEL0c1VHAwOVFXMmd2QjBTU0x6c056UUdkeVp3TG9Md3ZObVFIdWFobnlsbHlUQjEwSjlsUUlGUlNjZTZjRHg5Wmh3THhZdllXeGNYeENHQ2xESHp5RXgrdUJibzZWeVF4QnNwTVl4Yy9qZ01pS1VCOGU4dUwxOGVSOXh5b01kWm1GQVFxL2ZYUHFsZzllQjNPMEhMRG81OHVNalJIR0VRZElQOCtkRlNUVGVOcm1Bb2F4Smg5K3g0V3A0dUZzaklkOUhkSEVrbWhpekRBSGFpRmpaSEUvK2FuZGNnMEkyQzlKZEpocDVEUUVYbkpmWVFkOFBxbU5XVEREM214WjlXZDFZSGNFOGJldkhIb2IwbXFFL21VRHpSc3hvbTJKYUZNalIwVWxxWjM4V25jdzg5QjQvRGlXNEV3aTlobk9zQzA2Nk1CTjl1OUFFdHg2cU1PeWR3ZmtMZk9MVlovM2xkaFJHSGl4L2hadjJtbzBEU1pndnJYcG1zTFV5SDhXTHptWXlwNGNKdXVLQjF6WjNFSmxCMGMzZ1FHSmM4M2dzZmFkR1c3UTBwalRmWlIyblBITHlIQVVtWklUeFhZRT0mZ2hHRitXeVJpS29RRTd6cTRnK2hreTRvc05FPQ==',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'windows',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'x-twitter-active-user': 'yes',
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-client-language': 'en'
        }

ans = requests.get("https://www.pinterest.co.kr/search/pins/?q=charles%20leclerc&rs=typed",headers=header)
print(ans.text)

cookies = """
csrftoken=36965480027b268da1264bbd2aeb63b0; g_state={"i_l":0}; cm_sub=none; ar_debug=1; _routing_id="7d5cf6ad-02eb-46dd-97a3-8786200a7b3e"; sessionFunnelEventLogged=1; l_o=RlBVRVd0cHI0WUdvOTNtZklLRUxINnVSbVBOZDFzcFBlaGw4M1REampkUEV1TlBWb2NlWWtJQ1VLSjI1bnpKT2JReGU5Q2taTHY4OUwvVkkzeUkyMEJOVHpkYnVXaVBoVEZWUGZZWWFRc289JnJBUmZ6Mi9OSXU1VG80KzJMbExYc1lvUitGcz0=; _auth=1; _pinterest_sess=TWc9PSY4eWttUmVERGtIK09GNXB1TUZGcWhmZ2NyMnh3WitKclAvZHNCNFVLWk9JVzJZSVNvZWtkNXJLeEh6VXVncWtFTGNZVzgxTS9Cc0dYTkd5Z200V3hpMlQrdlU3dDR4K2hQZmFraEIzRkFwcnkyZ0VRa3MxWlhQVzlaS01UWTczS2YzWmNjczFNeWRxY3Z4aHZZNC9yV2pWaCtONnFmbHVyRjNjVlNoTDNHTjhuNEZVRSt0N2pZZzA5azkvdjI5UUpXaXdOTmMzaUhhR1ZWZU02a1k5TVV5aDlRNE55VFNXM2JWNVhGdE9IaUNJYWxmRUNXTFNSbVBiZWxKVFdYa29vT0JMUjVDTlVhTzFzNHp1cVlhcS9QUnArdGlJMTB0ZHNSVlMvYXhFZFZ6aC9jVUlLMG00emhSOWEza0xsZTdrd2RiMWZjV1RDNnJCeEJNQzRHb3ZFWnllb3ZoT1Z4SWFPV2cySkhhTGJIVmVQSTdlb3UyTHZUZ2Fxb0ZhTDJVY28xeE54YTlSdTlSVzFFUzdZOUJTMnJBdlBIYjNIK3RLMUVMNmxQU0lrUG81d2ZkU3o4ZXRrcFNleGZkUWRYZEUwa3kzUW1oWjdtVExHRGxOeDNiVzBPZGRFUVpmbGQ3eVFiNyt1Z0xuWDdKcDdhVWtwaThRT2hlczNlQUJaTDdOT3JmSnJwS1NCWWtjaHZoaW9rc2JNTUFvRFZiZndqL1hJQzRSSEpVRElzQ3o1TjJHbVhmTXZvV2NLaFV3bjkybDFlVTNvd0tRZ1c0U1hpQ1ZNYmNQY09aaDMvQ0pLaFVKenZCd2Q2Ujg3VGVTVUNYT3FNNjBSSUZoeE5tSzdmMmZhcU9NUVY5cS9uT1VraFNOQUZGY1Y4WFZKbFJIMlJUdnIrb0JjSkYrc2RvMmY1ZW8xZXlHeXcrWHlsZGhPTE1IRm1PQWpXS1V1WW55NTlWM09yZG5nU2F3T0VqRWx5Yzg3dDYyZVJqS0FDUDJXRXkvRzRBdFpEQ3UvTHlxYnVNb0NtZ2lBOEZvZ2xsUlFBbUtFTFoycGxyNUVSTWd3V1lnb1VuZnV5MTA1WnlvY0tBcFpuaDJjcFEzdWNGVVFqdG5CcHVtK093MnNHclNPeFptL2FLdUxKN010dG95UGt0azdjRk1yNGhwSVUzTzdtYzJ6N0I2Ukl1ZFZGSi8vdFM3Z2xmS1lKRGpVMHBQRjZjSXlRb0hJNXZqU21RSkU3cmRUQmlSZk14NnJJalEvR0pBSTZ2Ni9KaFZ2NW1GcnZFc0RpczNmM3VoVjZwcFJraU5HcktsRVQ4NDI4UTFMc0dybEhGUVN3bmNKeGY5eUZweUhkdS9LSG0wUW9Ja2pzenJ3by8xUG9pajdrVFVxZDVyaWlVa1dWczdGWXVyV1l6blNHN2dpWkZ6U0RoUkRUcjlmU0x4L3NxTFEzeFA4c0FBWW1yT3I1NERUUDhRaXhDeUNkZStFZ1Q2bFgxd1RrRlBrR1FTaFhxQ2c5c2hCRHdweWIwQStZYzNQNnhtbmtkLy9Ta1o2OFBJbHQrZXBBRzlsazIrcDUrUnVnR0lJUS92WTVDV1BHRlZEeUpsVUhtdUs3ZDJkcTFmaUkwWTFXVE0xSnRscExGYnYwMVVrTGNTVWpPdWVZSE1iQ0xCd1lKQWJWak5XdVVKYStIeXdsZEZjQkpJSlFQS0h2RVBKdGJ2V2xIQVRVbnpmSXFPLzREUlJGMHdiNnZzdkNQZTYvcEJZQkpLNmpYWGhiSUsvS0hHUzNLK2d4ZDdpVG5uc0xMbW4mSyt4T202WFFESDVjeXRNMlliSVJpN3RwZ2JRPQ==; __Secure-s_a=emQ4aERoMm1uams5MnBIY25aVGFJZU1EdThXSFB1UUlxQXlVdFBuNWlkbkFmMzl1OW1aRUFsb0VwelJjUzlMajM4NTNTcWRGSDlzbW9peGFUNllWZHQxK1FwdStyekRUTjJyOWtiUVFhUm42alp3VUpvOXppQW5XdWNHMFJXR3BmQm5KWTQveThLbmZqTkhJN3YwdHlPbkxqYkQrK0FXajhoSXpGL0ltYklGdkhMUWRNMFdrRjVvdEdoMHF4NUZWbTF4Q2J5T2N2Q3ZWYnZuYlZsNFRkRnRGNHFMM2lrZmlFV2Z1Y0pTWElUcVpzeHdESEU1NUhCbFZPUDVNMGFOaFdoalVKT3dib1A5ZmRHM0kwK0x5RkI0YXZqZlpWTVlKbWZtTWxCRU5KMVFpdi9PdnMwZEdqVjlsNS9aeUtqQnBadVUxcVhFbnVEZVZTdElmUUlVbmxkazV2K1d0VE9tOVlBMi9KbDdsQmovNWRDZWRXbGdpWmxMVlZMMzdKbjd0TW1TV2RzeGRYZUN0ZXluaFhZUGJaVDJMODRIaHdCU2E0azVXZmtacHNKUk1BOTBqZS83OGZEZGNXVTVVK0VlalFlV2E2VTNuNkxSTk84UGFPZnNpQnF2cEJDYm9LdUxMOWR3bXpRYm1kYmh3SERvc2ZvK0l5azVuVDRPdjJ3N3FDMW5oaW83UGp2SW1BSmxJTVlKQ0s1THZOYzlsdHV0aGFlSElFQ2pNVVJSVmpWL1kvMlc3UTh6N3E0eE9WdGw4Um5BVVQ0b0Vha1lwT09yRHFaL1Q2V2tVUkZjUWRYaG1DV1hYaEFad3pPWllvUFczZE93RzB3YmR1QlZFY0xuMnc5Q2kvaWRJQUltSTFzSTk1S1lhK3RQZUJjTC9EeUYrdFlEUWpNNzNqVm1SMm5XYjRaTDc0a3ZIOUdYYS9JR1h2SUtRSngzelF5VnlITVJVMVlIZnpEZ055WWJ4NnRCYXByT01EanA3djVTS1lhN1VEZnJTZkh3QnYwRUxFU2k5d25GaUJ4OUpNclp0Tis4ajYwbEIxWElvV0FuS1NTRHpIa3RIcjYybm5hRDF4emhMTEtXbm00OGVJaFI1ZER1enczQWRpSFRFTWVjWUNWRkw0RUk0SFpiTVAwaFNyeXVTV2lyakl6dm1sMHh6OEdMcjErU1VydTBSUzJVbnZYWVNSdmx4UkpqbmxOUWFRdk1rSW5jbWFlQ1EzVnlvSk9vNkNqaDRtS1h2c1Fuc0FzMHZIUmFEQksrYW1TVEQweldkbzJRaDgyeW00OUpGdjdWRjUvbVFOR2tPM3VPU3h2UmFqMi9KRW5CN0VCaz0mWThna0xDU3cySGZhWDRwQUo0bDEvdlM0M1NjPQ==
"""