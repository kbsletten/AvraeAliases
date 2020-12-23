embed
<drac2>
argv = &ARGS&
pairs = [(i, vroll(f"1d{len(argv)-i}+{i-1}").total) for i in range(0, len(argv)-1)]
for i, j in pairs:
  tmp = argv[i]
  argv[i] = argv[j]
  argv[j] = tmp
order = '\n'.join(argv)
</drac2>
-title "The party takes watches!"
-f "Order|{{order}}"
-footer "!watch"