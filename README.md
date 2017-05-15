# qmail-manager
It manages those qmail files.
A service responsible for managing a qmail dot files on disk.

### Running
In prod this uses veiux/sshfs to mount a remote ssh dir into a container. This is a volume plugin supported by docker. The service then hits the api and updates the files on disk, which are really on the qmail server. TODO: make this listen to alms for officer table updates. And TODO: have defaults in a config to make tech and technology and those ones work.
