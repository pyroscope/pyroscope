The following markup is supported:
```
=Heading1=
==Heading2==
===Heading3===

*bold* | _italic_ | `inline code` | escape: `*`

Lists:
 * bullet item
 * second
   * nested 1
   * nested 2
 * third
   * nested
 # numbered list
 # item 2

{{{
verbatim code block
}}}

WikiWordLink
[http://example.com/page Go to http://example.com/page]
http://example.com/page

Image
https://s3.amazonaws.com/cloud.ohloh.net/attachments/20048/ohloh_med.png

Horizontal rule
----
```

Tables are not supported and stay in their markup form.
What follows is a rendering of the above examples.

---

# Heading1 #
## Heading2 ##
### Heading3 ###

**bold** | _italic_ | `inline code` | escape: `*`

Lists:
  * bullet item
  * second
    * nested 1
    * nested 2
  * third
    * nested
  1. numbered list
  1. item 2

```
verbatim code block
```

WikiWordLink
[Go to http://example.com/page](http://example.com/page)
http://example.com/page

Image
![https://s3.amazonaws.com/cloud.ohloh.net/attachments/20048/ohloh_med.png](https://s3.amazonaws.com/cloud.ohloh.net/attachments/20048/ohloh_med.png)

Horizontal rule

---
