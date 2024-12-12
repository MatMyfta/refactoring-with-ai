
public class Sample {
    // @BUG: NullPointerException might occur
    public int add(int a, int b) {
        return a + b;
    }

    /*
    @HACK: Temporary fix for performance issue
    */
    public void process() {
        // processing logic
    }
}