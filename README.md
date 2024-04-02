# Ansible Collection - bodsch.email


This collection aims to provide a set of small Ansible modules and helper functions.

## Included content

### Modules

| Name                      | Description |
|:--------------------------|:----|


## Installing this collection

You can install the memsource collection with the Ansible Galaxy CLI:

```sh
#> ansible-galaxy collection install bodsch.email
```

To install directly from GitHub:

```sh
#> ansible-galaxy collection install git@github.com:bodsch/ansible-collection-email.git
```


You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: bodsch.email
```

The python module dependencies are not installed by `ansible-galaxy`.  They can
be manually installed using pip:

```sh
#> pip install -r requirements.txt
```

## Using this collection


You can either call modules by their Fully Qualified Collection Namespace (FQCN), such as `bodsch.email.postfix`,
or you can call modules by their short name if you list the `bodsch.email` collection in the playbook's `collections` keyword:

```yaml
---

```


## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://github.com/bodsch/ansible-collection-email/tags)!


## Author

- Bodo Schulz

## License

[Apache](LICENSE)

**FREE SOFTWARE, HELL YEAH!**
