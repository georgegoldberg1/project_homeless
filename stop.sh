docker stop base_python \
	&& echo 'container "base_python" stopped. You can can run jupyter in docker using "bash go.sh"' \
	|| echo 'container was not running. You can can run jupyter in docker using "bash go.sh"'
