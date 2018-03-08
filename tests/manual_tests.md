# Manual Tests for cards

*Probably haven't seen many open source projects with manual test procedures, have you?*

*This makes more sense in the context of the podcast. See [Test & Code, episode 37](http://testandcode.com/37)*

So far, just one test.

1. ALAC Test 1

    Examples shown don't have to be followed exactly.

    1. Add 3 items:

        ~~~
        $ cards add something
        $ cards add "something else"
        $ cards add "Foo Bar Baz"
        ~~~

    2. Make sure they show up in the list:
        ~~~
        $ cards list
         ID      owner  done summary
         --      -----  ---- -------
          1                  something
          2                  something else
          3                  Foo Bar Baz
        ~~~

    3. Change the owner on a card. Verify change.
    4. Change the done state on a card. Verify change.
    5. Change the sumary on a card. Verify change.

        ~~~
        $ cards update --owner okken 1
        $ cards update --done True 2
        $ cards update --summary "just sit" 3
        $ cards list
          ID      owner  done summary
          --      -----  ---- -------
           1      okken       something
           2               x  something else
           3                  just sit
        ~~~

    6. Delete the done item. Verify change.

        ~~~
        (cards) $ cards delete 2
        (cards) $ cards list
          ID      owner  done summary
          --      -----  ---- -------
           1      okken       something
           3                  just sit
        ~~~


